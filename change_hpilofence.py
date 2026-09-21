#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HPE BladeSystem c7000
Parallel hpilofence account creation / permission correction

Purpose
-------
1. Detect the ACTIVE OA.
2. Discover all blade servers.
3. Process blades in parallel using a ThreadPoolExecutor.
4. Each worker creates its own SSH connection to the ACTIVE OA.
5. For every blade:

       GET_USER
           |
           +-- account exists
           |      |
           |      +-- already Operator -> verify
           |      |
           |      +-- not Operator -> MOD_USER -> verify
           |
           +-- account missing -> ADD_USER -> verify

Target iLO/IPMI privilege level:

    OPERATOR

Target privileges:

    Administer User Accounts : NO
    Remote Console Access    : YES
    Virtual Power and Reset  : YES
    Virtual Media            : YES
    Configure iLO Settings   : NO

IMPORTANT
---------
This script does NOT automatically power-cycle blades.

Concurrency
-----------
Default:

    MAX_WORKERS = 4

Each worker uses its own SSH session to the ACTIVE OA.

Python:
    Compatible with Python 3.6+
"""

# ============================================================================
# IMPORTS
# ============================================================================

import os
import sys
import time
import re
import logging
import warnings

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# Suppress Python 3.6 / cryptography warnings.
os.environ["PYTHONWARNINGS"] = "ignore"

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import cryptography
except Exception:
    pass

import paramiko

from xml.sax.saxutils import escape as xml_escape

from functions import vars


# ============================================================================
# CONFIGURATION
# ============================================================================

# ---------------------------------------------------------------------------
# OA IP addresses
# ---------------------------------------------------------------------------

OA1_IP = "10.101.18.35"
OA2_IP = "10.101.18.36"

OA1_BAY = 1
OA2_BAY = 2


# ---------------------------------------------------------------------------
# PARALLEL EXECUTION
# ---------------------------------------------------------------------------

# Number of blades processed simultaneously.
#
# Start with 4.
#
# If the OA is stable and you want more concurrency, try 6.
# I do NOT recommend immediately jumping to 16.
#
MAX_WORKERS = 8


# ---------------------------------------------------------------------------
# OA credentials
# ---------------------------------------------------------------------------

OA_USERNAME = vars.OA_USERNAME
OA_PASSWORD = vars.OA_PASSWORD


# ---------------------------------------------------------------------------
# Fence account
# ---------------------------------------------------------------------------

FENCE_USER_NAME = vars.FENCE_USER_NAME
FENCE_USER_LOGIN = vars.FENCE_USER_LOGIN
FENCE_USER_PASSWORD = vars.FENCE_USER_PASSWORD


# ---------------------------------------------------------------------------
# SSH / HPONCFG settings
#
# These are taken from vars.py / configure_ilo_BL.py.
# ---------------------------------------------------------------------------

SSH_PORT = vars.ILO_BL_SSH_PORT
SSH_CONNECT_TIMEOUT = vars.ILO_BL_SSH_CONNECT_TIMEOUT
SSH_KEEPALIVE_INTERVAL = vars.ILO_BL_SSH_KEEPALIVE_INTERVAL

COMMAND_TIMEOUT = vars.ILO_BL_COMMAND_TIMEOUT
COMMAND_QUIET_TIME = vars.ILO_BL_COMMAND_QUIET_TIME
HPONCFG_LINE_DELAY = vars.ILO_BL_HPONCFG_LINE_DELAY


# ---------------------------------------------------------------------------
# RIBCL retry settings
# ---------------------------------------------------------------------------

RIBCL_RETRIES = 3
RIBCL_RETRY_DELAY = 3


# ---------------------------------------------------------------------------
# Optional IPMI verification
# ---------------------------------------------------------------------------

VERIFY_IPMI = False

IPMI_CIPHER = "3"


# ============================================================================
# TARGET OPERATOR PRIVILEGES
# ============================================================================

OPERATOR_PRIVILEGES = {
    "ADMIN_PRIV": "N",
    "REMOTE_CONS_PRIV": "Y",
    "RESET_SERVER_PRIV": "Y",
    "VIRTUAL_MEDIA_PRIV": "Y",
    "CONFIG_ILO_PRIV": "N",
}


# ============================================================================
# LOGGING
# ============================================================================

logger = logging.getLogger("hpilofence")

logger.setLevel(logging.DEBUG)

logger.propagate = False

if not logger.handlers:

    handler = logging.StreamHandler(sys.stdout)

    handler.setLevel(logging.INFO)

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s"
        )
    )

    logger.addHandler(handler)


# ============================================================================
# GENERAL HELPERS
# ============================================================================

def log_slot(slot, message):

    try:
        slot_number = int(slot)
        slot_text = "{:02d}".format(slot_number)

    except Exception:
        slot_text = "??"

    logger.info(
        "[Slot %s] %s",
        slot_text,
        message
    )


def xml_attr(value):

    return xml_escape(
        str(value),
        {
            '"': "&quot;",
            "'": "&apos;",
        }
    )


def normalize_boolean(value):

    value = str(value or "").strip().upper()

    if value in (
        "Y",
        "YES",
        "TRUE",
        "1",
    ):
        return "Y"

    if value in (
        "N",
        "NO",
        "FALSE",
        "0",
    ):
        return "N"

    return value


# ============================================================================
# RIBCL BUILDERS
# ============================================================================

def build_ribcl_user_check():

    return """<RIBCL VERSION="2.0">
<LOGIN USER_LOGIN="{oa_user}" PASSWORD="{oa_password}">
<USER_INFO MODE="read">
<GET_USER USER_LOGIN="{fence_user}"/>
</USER_INFO>
</LOGIN>
</RIBCL>""".format(
        oa_user=xml_attr(OA_USERNAME),
        oa_password=xml_attr(OA_PASSWORD),
        fence_user=xml_attr(FENCE_USER_LOGIN),
    )


def build_ribcl_user_add():

    p = OPERATOR_PRIVILEGES

    return """<RIBCL VERSION="2.0">
<LOGIN USER_LOGIN="{oa_user}" PASSWORD="{oa_password}">
<USER_INFO MODE="write">
<ADD_USER
    USER_NAME="{friendly_name}"
    USER_LOGIN="{login_name}"
    PASSWORD="{password}">
<ADMIN_PRIV VALUE="{admin_priv}"/>
<REMOTE_CONS_PRIV VALUE="{remote_console}"/>
<RESET_SERVER_PRIV VALUE="{reset_server}"/>
<VIRTUAL_MEDIA_PRIV VALUE="{virtual_media}"/>
<CONFIG_ILO_PRIV VALUE="{config_ilo}"/>
</ADD_USER>
</USER_INFO>
</LOGIN>
</RIBCL>""".format(
        oa_user=xml_attr(OA_USERNAME),
        oa_password=xml_attr(OA_PASSWORD),
        friendly_name=xml_attr(FENCE_USER_NAME),
        login_name=xml_attr(FENCE_USER_LOGIN),
        password=xml_attr(FENCE_USER_PASSWORD),
        admin_priv=p["ADMIN_PRIV"],
        remote_console=p["REMOTE_CONS_PRIV"],
        reset_server=p["RESET_SERVER_PRIV"],
        virtual_media=p["VIRTUAL_MEDIA_PRIV"],
        config_ilo=p["CONFIG_ILO_PRIV"],
    )


def build_ribcl_user_modify():

    p = OPERATOR_PRIVILEGES

    return """<RIBCL VERSION="2.0">
<LOGIN USER_LOGIN="{oa_user}" PASSWORD="{oa_password}">
<USER_INFO MODE="write">
<MOD_USER USER_LOGIN="{login_name}">
<ADMIN_PRIV VALUE="{admin_priv}"/>
<REMOTE_CONS_PRIV VALUE="{remote_console}"/>
<RESET_SERVER_PRIV VALUE="{reset_server}"/>
<VIRTUAL_MEDIA_PRIV VALUE="{virtual_media}"/>
<CONFIG_ILO_PRIV VALUE="{config_ilo}"/>
</MOD_USER>
</USER_INFO>
</LOGIN>
</RIBCL>""".format(
        oa_user=xml_attr(OA_USERNAME),
        oa_password=xml_attr(OA_PASSWORD),
        login_name=xml_attr(FENCE_USER_LOGIN),
        admin_priv=p["ADMIN_PRIV"],
        remote_console=p["REMOTE_CONS_PRIV"],
        reset_server=p["RESET_SERVER_PRIV"],
        virtual_media=p["VIRTUAL_MEDIA_PRIV"],
        config_ilo=p["CONFIG_ILO_PRIV"],
    )


# ============================================================================
# RIBCL PARSING
# ============================================================================

def extract_ribcl_results(output):

    if not output:
        return ""

    match = re.search(
        r"START\s+RIBCL\s+RESULTS"
        r".*?"
        r"(.*?)"
        r"(?:END\s+RIBCL\s+RESULTS|$)",
        output,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1)

    return output


def normalize_ribcl_status(status):

    value = str(status or "").strip().upper()

    value = value.replace(
        "0X",
        ""
    )

    try:

        return "0X{:04X}".format(
            int(value, 16)
        )

    except Exception:

        return value


def parse_ribcl_responses(output):

    result_text = extract_ribcl_results(
        output
    )

    responses = []

    response_tags = re.findall(
        r"<RESPONSE\b(.*?)/>",
        result_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    for tag in response_tags:

        status_match = re.search(
            r'\bSTATUS\s*=\s*["\']([^"\']+)["\']',
            tag,
            flags=re.IGNORECASE,
        )

        message_match = re.search(
            r'\b(?:MSG|MESSAGE)\s*=\s*["\']([^"\']*)["\']',
            tag,
            flags=re.IGNORECASE,
        )

        if status_match:

            status = normalize_ribcl_status(
                status_match.group(1)
            )

        else:

            status = "UNKNOWN"

        if message_match:

            message = message_match.group(1).strip()

        else:

            message = ""

        responses.append(
            (
                status,
                message
            )
        )

    return responses


def ribcl_errors(
    output,
    allowed_statuses=("0X0000",)
):

    allowed = set(
        normalize_ribcl_status(x)
        for x in allowed_statuses
    )

    responses = parse_ribcl_responses(
        output
    )

    if not responses:

        return [
            "No RIBCL RESPONSE elements returned"
        ]

    errors = []

    for status, message in responses:

        if status not in allowed:

            errors.append(
                "{}: {}".format(
                    status,
                    message or "Unknown error"
                )
            )

    return errors


# ============================================================================
# GET_USER PARSING
# ============================================================================

def parse_get_user(output):

    result_text = extract_ribcl_results(
        output
    )

    get_user_tags = re.findall(
        r"<GET_USER\b([^>]*)/?>",
        result_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    for tag in get_user_tags:

        login_match = re.search(
            r'\bUSER_LOGIN\s*=\s*["\']([^"\']+)["\']',
            tag,
            flags=re.IGNORECASE,
        )

        if not login_match:
            continue

        login = login_match.group(1).strip()

        if login.lower() != FENCE_USER_LOGIN.lower():
            continue

        privileges = {}

        fields = [
            "ADMIN_PRIV",
            "REMOTE_CONS_PRIV",
            "RESET_SERVER_PRIV",
            "VIRTUAL_MEDIA_PRIV",
            "CONFIG_ILO_PRIV",
        ]

        for field in fields:

            match = re.search(
                r'\b{}\s*=\s*["\']([^"\']+)["\']'.format(
                    field
                ),
                tag,
                flags=re.IGNORECASE,
            )

            if match:

                privileges[field] = normalize_boolean(
                    match.group(1)
                )

        return {
            "exists": True,
            "privileges": privileges,
            "error": None,
        }

    # Account does not exist.
    if re.search(
        r"(?:User\s+login\s+name\s+was\s+not\s+found|"
        r"user.*not.*found|"
        r"login.*not.*found)",
        result_text,
        flags=re.IGNORECASE,
    ):

        return {
            "exists": False,
            "privileges": {},
            "error": "not found",
        }

    errors = ribcl_errors(
        output
    )

    if errors:

        return {
            "exists": False,
            "privileges": {},
            "error": "; ".join(errors),
        }

    return {
        "exists": False,
        "privileges": {},
        "error": (
            "GET_USER completed successfully "
            "but did not return the account"
        ),
    }


def format_privileges(privileges):

    return (
        "ADMIN_PRIV={admin}, "
        "REMOTE_CONS_PRIV={remote}, "
        "RESET_SERVER_PRIV={reset}, "
        "VIRTUAL_MEDIA_PRIV={media}, "
        "CONFIG_ILO_PRIV={config}"
    ).format(
        admin=privileges.get(
            "ADMIN_PRIV",
            "?"
        ),
        remote=privileges.get(
            "REMOTE_CONS_PRIV",
            "?"
        ),
        reset=privileges.get(
            "RESET_SERVER_PRIV",
            "?"
        ),
        media=privileges.get(
            "VIRTUAL_MEDIA_PRIV",
            "?"
        ),
        config=privileges.get(
            "CONFIG_ILO_PRIV",
            "?"
        ),
    )


def privileges_are_operator(privileges):

    for key, expected in OPERATOR_PRIVILEGES.items():

        actual = normalize_boolean(
            privileges.get(
                key,
                ""
            )
        )

        if actual != expected:

            return False

    return True


# ============================================================================
# OA CONNECTION
# ============================================================================

class OAConnection(object):

    def __init__(
        self,
        username,
        password,
        port=22
    ):

        self.username = username
        self.password = password
        self.port = port

        self.client = None
        self.channel = None

    def connect(self, hostname):

        self.close()

        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.client.connect(
            hostname=hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=SSH_CONNECT_TIMEOUT,
            banner_timeout=SSH_CONNECT_TIMEOUT,
            auth_timeout=SSH_CONNECT_TIMEOUT,
            look_for_keys=False,
            allow_agent=False,
        )

        transport = self.client.get_transport()

        if transport:

            transport.set_keepalive(
                SSH_KEEPALIVE_INTERVAL
            )

        self.channel = self.client.invoke_shell()

        time.sleep(0.5)

        self._drain_channel()

    def close(self):

        if self.channel:

            try:
                self.channel.close()

            except Exception:
                pass

        self.channel = None

        if self.client:

            try:
                self.client.close()

            except Exception:
                pass

        self.client = None

    def _drain_channel(self):

        if not self.channel:

            return ""

        output = ""

        while self.channel.recv_ready():

            data = self.channel.recv(
                65535
            )

            if not data:

                break

            output += data.decode(
                "utf-8",
                errors="replace"
            )

        return output

    def send_command(
        self,
        command,
        wait_string=">",
        timeout=15
    ):

        if not self.channel:

            raise RuntimeError(
                "OA SSH channel is not connected"
            )

        self._drain_channel()

        self.channel.sendall(
            command + "\n"
        )

        output = ""

        deadline = (
            time.monotonic()
            + timeout
        )

        while time.monotonic() < deadline:

            if self.channel.recv_ready():

                data = self.channel.recv(
                    65535
                )

                if not data:

                    break

                output += data.decode(
                    "utf-8",
                    errors="replace"
                )

                if wait_string in output:

                    time.sleep(0.1)

                    while self.channel.recv_ready():

                        more = self.channel.recv(
                            65535
                        )

                        if not more:

                            break

                        output += more.decode(
                            "utf-8",
                            errors="replace"
                        )

                    break

            else:

                time.sleep(0.05)

        return output

    def execute_hponcfg(
        self,
        bay_number,
        ribcl,
        end_marker="ILO_RIBCL_EOF"
    ):

        if not self.channel:

            raise RuntimeError(
                "OA SSH channel is not connected"
            )

        bay_number = int(
            bay_number
        )

        self._drain_channel()

        command = (
            "HPONCFG {bay} << {marker}\n"
            "{ribcl}\n"
            "{marker}\n"
        ).format(
            bay=bay_number,
            marker=end_marker,
            ribcl=ribcl.rstrip(),
        )

        # Send the command line-by-line.
        for line in command.splitlines():

            self.channel.sendall(
                line + "\n"
            )

            time.sleep(
                HPONCFG_LINE_DELAY
            )

        output = ""

        deadline = (
            time.monotonic()
            + COMMAND_TIMEOUT
        )

        quiet_since = None

        while time.monotonic() < deadline:

            if self.channel.recv_ready():

                data = self.channel.recv(
                    65535
                )

                if not data:

                    break

                output += data.decode(
                    "utf-8",
                    errors="replace"
                )

                quiet_since = None

                # Normal RIBCL completion.
                if re.search(
                    r"END\s+RIBCL\s+RESULTS",
                    output,
                    flags=re.IGNORECASE,
                ):

                    time.sleep(0.1)

                    while self.channel.recv_ready():

                        more = self.channel.recv(
                            65535
                        )

                        if not more:

                            break

                        output += more.decode(
                            "utf-8",
                            errors="replace"
                        )

                    break

            else:

                if quiet_since is None:

                    quiet_since = time.monotonic()

                elif (
                    time.monotonic()
                    - quiet_since
                    >= COMMAND_QUIET_TIME
                ):

                    break

                time.sleep(0.05)

        return output


# ============================================================================
# ACTIVE OA
# ============================================================================

def find_active_oa():

    candidates = [
        (
            OA1_IP,
            OA1_BAY
        ),
        (
            OA2_IP,
            OA2_BAY
        ),
    ]

    for ip, bay in candidates:

        logger.info(
            ""
        )

        logger.info(
            "Checking OA%d at %s...",
            bay,
            ip
        )

        oa = OAConnection(
            OA_USERNAME,
            OA_PASSWORD,
            SSH_PORT,
        )

        try:

            oa.connect(
                ip
            )

            output = oa.send_command(
                "SHOW OA STATUS {}".format(
                    bay
                ),
                timeout=15,
            )

            if re.search(
                r"\bRole:\s*Active\b",
                output,
                flags=re.IGNORECASE,
            ):

                logger.info(
                    "SUCCESS: OA%d (%s) is ACTIVE.",
                    bay,
                    ip
                )

                return oa, ip, bay

            logger.info(
                "OA%d (%s) is STANDBY.",
                bay,
                ip
            )

            oa.close()

        except Exception as exc:

            logger.error(
                "OA%d (%s) check failed: %s",
                bay,
                ip,
                exc
            )

            oa.close()

    return None, None, None


# ============================================================================
# BLADE DISCOVERY
# ============================================================================

def discover_blades(oa):

    logger.info(
        ""
    )

    logger.info(
        "Discovering blade servers..."
    )

    output = oa.send_command(
        "SHOW SERVER LIST",
        timeout=30,
    )

    if re.search(
        r"running in standby mode",
        output,
        flags=re.IGNORECASE,
    ):

        raise RuntimeError(
            "Connected OA is standby. "
            "Cannot execute SHOW SERVER LIST."
        )

    logger.info(
        ""
    )

    logger.info(
        "OA SERVER LIST:"
    )

    logger.info(
        "%s",
        output.strip()
    )

    blades = []

    pattern = re.compile(
        r"^\s*"
        r"(\d+)"
        r"\s+"
        r"(\S+)"
        r"\s+"
        r"(\d{1,3}(?:\.\d{1,3}){3})"
        r"\s+"
        r"(\S+)"
        r"\s+"
        r"(\S+)"
        r"\s+"
        r"(\S+)"
        r"(?:\s+(.*?))?"
        r"\s*$",
        flags=re.IGNORECASE,
    )

    for line in output.splitlines():

        match = pattern.match(
            line
        )

        if not match:

            continue

        slot = int(
            match.group(1)
        )

        if not 1 <= slot <= 16:

            continue

        blades.append(
            {
                "slot": slot,
                "ilo_name": match.group(2),
                "ilo_ip": match.group(3),
                "status": match.group(4),
                "power": match.group(5),
                "uid": match.group(6),
                "partner": (
                    match.group(7)
                    or ""
                ).strip(),
            }
        )

    blades.sort(
        key=lambda item: item["slot"]
    )

    logger.info(
        ""
    )

    logger.info(
        "Discovered %d blade(s).",
        len(blades)
    )

    return blades


# ============================================================================
# RIBCL EXECUTION
# ============================================================================

def execute_ribcl(
    oa,
    blade,
    ribcl,
    end_marker,
    operation
):

    slot = blade["slot"]

    last_output = ""

    for attempt in range(
        1,
        RIBCL_RETRIES + 1
    ):

        log_slot(
            slot,
            "{} - attempt {}/{}".format(
                operation,
                attempt,
                RIBCL_RETRIES
            )
        )

        try:

            output = oa.execute_hponcfg(
                slot,
                ribcl,
                end_marker=end_marker,
            )

            last_output = output

            errors = ribcl_errors(
                output
            )

            if not errors:

                return output, None

            if (
                len(errors) == 1
                and
                errors[0]
                == "No RIBCL RESPONSE elements returned"
            ):

                log_slot(
                    slot,
                    "No RIBCL response received."
                )

            else:

                return (
                    output,
                    "; ".join(
                        errors
                    )
                )

        except Exception as exc:

            log_slot(
                slot,
                "{} failed: {}".format(
                    operation,
                    exc
                )
            )

        if attempt < RIBCL_RETRIES:

            time.sleep(
                RIBCL_RETRY_DELAY
            )

    errors = ribcl_errors(
        last_output
    )

    if errors:

        return (
            last_output,
            "; ".join(errors)
        )

    return (
        last_output,
        "{} failed".format(
            operation
        )
    )


# ============================================================================
# CHECK ACCOUNT
# ============================================================================

def check_account(
    oa,
    blade
):

    slot = blade["slot"]

    log_slot(
        slot,
        "Checking whether '{}' exists...".format(
            FENCE_USER_LOGIN
        )
    )

    output, error = execute_ribcl(
        oa,
        blade,
        build_ribcl_user_check(),
        "ILO_FENCE_USER_CHECK_EOF",
        "GET_USER",
    )

    if error:

        return {
            "success": False,
            "exists": None,
            "privileges": {},
            "error": error,
        }

    result = parse_get_user(
        output
    )

    if result["exists"]:

        log_slot(
            slot,
            "Account '{}' exists.".format(
                FENCE_USER_LOGIN
            )
        )

        log_slot(
            slot,
            "Current privileges: {}".format(
                format_privileges(
                    result["privileges"]
                )
            )
        )

        return {
            "success": True,
            "exists": True,
            "privileges": result[
                "privileges"
            ],
            "error": None,
        }

    if result["error"] == "not found":

        log_slot(
            slot,
            "Account '{}' does not exist.".format(
                FENCE_USER_LOGIN
            )
        )

        return {
            "success": True,
            "exists": False,
            "privileges": {},
            "error": None,
        }

    return {
        "success": False,
        "exists": None,
        "privileges": {},
        "error": result[
            "error"
        ],
    }


# ============================================================================
# CREATE ACCOUNT
# ============================================================================

def create_account(
    oa,
    blade
):

    slot = blade["slot"]

    log_slot(
        slot,
        "Creating '{}' as OPERATOR...".format(
            FENCE_USER_LOGIN
        )
    )

    log_slot(
        slot,
        "Target privileges: {}".format(
            format_privileges(
                OPERATOR_PRIVILEGES
            )
        )
    )

    output, error = execute_ribcl(
        oa,
        blade,
        build_ribcl_user_add(),
        "ILO_FENCE_USER_ADD_EOF",
        "ADD_USER",
    )

    if error:

        log_slot(
            slot,
            "ADD_USER returned: {}".format(
                error
            )
        )

        # Check whether account was actually created.
        verification = check_account(
            oa,
            blade
        )

        if (
            verification["success"]
            and
            verification["exists"]
        ):

            log_slot(
                slot,
                "Account exists after ADD_USER."
            )

            return True

        return False

    log_slot(
        slot,
        "ADD_USER completed successfully."
    )

    return True


# ============================================================================
# MODIFY ACCOUNT
# ============================================================================

def modify_account(
    oa,
    blade
):

    slot = blade["slot"]

    log_slot(
        slot,
        "Modifying existing '{}' permissions...".format(
            FENCE_USER_LOGIN
        )
    )

    log_slot(
        slot,
        "Target privileges: {}".format(
            format_privileges(
                OPERATOR_PRIVILEGES
            )
        )
    )

    output, error = execute_ribcl(
        oa,
        blade,
        build_ribcl_user_modify(),
        "ILO_FENCE_USER_MOD_EOF",
        "MOD_USER",
    )

    if error:

        log_slot(
            slot,
            "Permission update FAILED: {}".format(
                error
            )
        )

        return False

    log_slot(
        slot,
        "MOD_USER completed successfully."
    )

    return True


# ============================================================================
# FINAL VERIFICATION
# ============================================================================

def verify_operator(
    oa,
    blade
):

    slot = blade["slot"]

    log_slot(
        slot,
        "Verifying final '{}' privileges...".format(
            FENCE_USER_LOGIN
        )
    )

    time.sleep(1)

    result = check_account(
        oa,
        blade
    )

    if not result["success"]:

        log_slot(
            slot,
            "Verification FAILED: {}".format(
                result["error"]
            )
        )

        return False, result

    if not result["exists"]:

        log_slot(
            slot,
            "Verification FAILED: account does not exist."
        )

        return False, result

    privileges = result[
        "privileges"
    ]

    logger.info(
        "[Slot %02d] FINAL hpilofence privileges: %s",
        slot,
        format_privileges(
            privileges
        )
    )

    if privileges_are_operator(
        privileges
    ):

        log_slot(
            slot,
            "SUCCESS: hpilofence is configured as OPERATOR."
        )

        return True, result

    log_slot(
        slot,
        "FAILED: hpilofence is NOT OPERATOR."
    )

    log_slot(
        slot,
        "Expected: {}".format(
            format_privileges(
                OPERATOR_PRIVILEGES
            )
        )
    )

    log_slot(
        slot,
        "Actual: {}".format(
            format_privileges(
                privileges
            )
        )
    )

    return False, result


# ============================================================================
# OPTIONAL IPMI VERIFICATION
# ============================================================================

def verify_ipmi_operator(
    blade
):

    if not VERIFY_IPMI:

        return True

    import subprocess

    slot = blade["slot"]
    ilo_ip = blade["ilo_ip"]

    log_slot(
        slot,
        "Testing IPMI Operator access..."
    )

    command = [
        "fence_ilo4",
        "-a",
        ilo_ip,
        "-l",
        FENCE_USER_LOGIN,
        "-p",
        FENCE_USER_PASSWORD,
        "-L",
        "operator",
        "-C",
        IPMI_CIPHER,
        "-o",
        "status",
    ]

    try:

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=60,
        )

        output = result.stdout or ""

        for line in output.splitlines():

            log_slot(
                slot,
                line
            )

        if (
            result.returncode == 0
            and
            re.search(
                r"\bStatus:\s*(ON|OFF)\b",
                output,
                flags=re.IGNORECASE,
            )
        ):

            log_slot(
                slot,
                "IPMI OPERATOR verification successful."
            )

            return True

        log_slot(
            slot,
            "IPMI OPERATOR verification FAILED."
        )

        return False

    except Exception as exc:

        log_slot(
            slot,
            "IPMI verification error: {}".format(
                exc
            )
        )

        return False


# ============================================================================
# PROCESS ONE BLADE
# ============================================================================

def process_blade(
    active_oa_ip,
    blade
):
    """
    Each worker creates its OWN SSH connection.

    This is critical.

    We never share one Paramiko channel between worker threads.
    """

    slot = blade["slot"]

    ilo_name = blade["ilo_name"]

    ilo_ip = blade["ilo_ip"]

    worker_oa = None

    try:

        logger.info(
            ""
        )

        logger.info(
            "[Slot %02d] ================================================",
            slot
        )

        logger.info(
            "[Slot %02d] Processing %s",
            slot,
            ilo_name
        )

        logger.info(
            "[Slot %02d] iLO IP : %s",
            slot,
            ilo_ip
        )

        logger.info(
            "[Slot %02d] Worker connecting to active OA %s",
            slot,
            active_oa_ip
        )

        # ---------------------------------------------------------------
        # Each thread has its own SSH connection.
        # ---------------------------------------------------------------

        worker_oa = OAConnection(
            OA_USERNAME,
            OA_PASSWORD,
            SSH_PORT,
        )

        worker_oa.connect(
            active_oa_ip
        )

        log_slot(
            slot,
            "Connected to active OA."
        )

        # ---------------------------------------------------------------
        # STEP 1 - Check account
        # ---------------------------------------------------------------

        check = check_account(
            worker_oa,
            blade
        )

        if not check["success"]:

            return {
                "slot": slot,
                "ilo_name": ilo_name,
                "ilo_ip": ilo_ip,
                "status": "ERROR",
                "message": (
                    "Unable to determine whether "
                    "account exists: {}"
                ).format(
                    check["error"]
                ),
            }

        # ---------------------------------------------------------------
        # STEP 2 - Existing account
        # ---------------------------------------------------------------

        if check["exists"]:

            if privileges_are_operator(
                check["privileges"]
            ):

                log_slot(
                    slot,
                    "Account already has OPERATOR privileges."
                )

            else:

                log_slot(
                    slot,
                    "Existing privileges are incorrect."
                )

                if not modify_account(
                    worker_oa,
                    blade
                ):

                    return {
                        "slot": slot,
                        "ilo_name": ilo_name,
                        "ilo_ip": ilo_ip,
                        "status": "FAILED",
                        "message": (
                            "RIBCL permission update failed."
                        ),
                    }

        # ---------------------------------------------------------------
        # STEP 3 - Account missing
        # ---------------------------------------------------------------

        else:

            if not create_account(
                worker_oa,
                blade
            ):

                return {
                    "slot": slot,
                    "ilo_name": ilo_name,
                    "ilo_ip": ilo_ip,
                    "status": "FAILED",
                    "message": (
                        "RIBCL account creation failed."
                    ),
                }

        # ---------------------------------------------------------------
        # STEP 4 - Mandatory final verification
        # ---------------------------------------------------------------

        verified, verification = verify_operator(
            worker_oa,
            blade
        )

        if not verified:

            return {
                "slot": slot,
                "ilo_name": ilo_name,
                "ilo_ip": ilo_ip,
                "status": "FAILED",
                "message": (
                    "Account was configured but "
                    "final privilege verification failed."
                ),
            }

        # ---------------------------------------------------------------
        # STEP 5 - Optional IPMI verification
        # ---------------------------------------------------------------

        if VERIFY_IPMI:

            if not verify_ipmi_operator(
                blade
            ):

                return {
                    "slot": slot,
                    "ilo_name": ilo_name,
                    "ilo_ip": ilo_ip,
                    "status": "FAILED",
                    "message": (
                        "RIBCL privileges are correct "
                        "but IPMI Operator verification failed."
                    ),
                }

        # ---------------------------------------------------------------
        # SUCCESS
        # ---------------------------------------------------------------

        if check["exists"]:

            message = (
                "Existing hpilofence permissions "
                "modified and verified as OPERATOR."
            )

        else:

            message = (
                "hpilofence created and verified "
                "as OPERATOR."
            )

        return {
            "slot": slot,
            "ilo_name": ilo_name,
            "ilo_ip": ilo_ip,
            "status": "OK",
            "message": message,
        }

    except Exception as exc:

        logger.exception(
            "[Slot %02d] Worker failed: %s",
            slot,
            exc
        )

        return {
            "slot": slot,
            "ilo_name": ilo_name,
            "ilo_ip": ilo_ip,
            "status": "ERROR",
            "message": str(exc),
        }

    finally:

        if worker_oa:

            try:

                worker_oa.close()

            except Exception:

                pass

            log_slot(
                slot,
                "Worker OA connection closed."
            )


# ============================================================================
# FINAL REPORT
# ============================================================================

def print_final_report(
    results
):

    logger.info("")
    logger.info(
        "=" * 80
    )

    logger.info(
        "FINAL RESULT"
    )

    logger.info(
        "=" * 80
    )

    for result in sorted(
        results,
        key=lambda item: item["slot"]
    ):

        logger.info(
            "Slot %02d | %-20s | %-15s | %-8s | %s",
            result["slot"],
            result["ilo_name"],
            result["ilo_ip"],
            result["status"],
            result["message"],
        )

    logger.info(
        "=" * 80
    )

    ok_count = sum(
        1
        for result in results
        if result["status"] == "OK"
    )

    error_count = sum(
        1
        for result in results
        if result["status"] == "ERROR"
    )

    failed_count = sum(
        1
        for result in results
        if result["status"] == "FAILED"
    )

    logger.info(
        "OK       : %d",
        ok_count
    )

    logger.info(
        "ERROR    : %d",
        error_count
    )

    logger.info(
        "FAILED   : %d",
        failed_count
    )

    logger.info(
        "TOTAL    : %d",
        len(results)
    )

    logger.info(
        "=" * 80
    )

    return (
        failed_count == 0
        and
        error_count == 0
    )


# ============================================================================
# MAIN
# ============================================================================

def main():

    start_time = time.time()

    logger.info(
        "=" * 80
    )

    logger.info(
        "HPE iLO HPILOFENCE OPERATOR CONFIGURATION"
    )

    logger.info(
        "PARALLEL / THREADED MODE"
    )

    logger.info(
        "=" * 80
    )

    logger.info(
        "Fence account : %s",
        FENCE_USER_LOGIN
    )

    logger.info(
        "Friendly name : %s",
        FENCE_USER_NAME
    )

    logger.info(
        "Target role   : OPERATOR"
    )

    logger.info(
        "Worker threads: %d",
        MAX_WORKERS
    )

    logger.info(
        ""
    )

    logger.info(
        "Target privileges:"
    )

    logger.info(
        "  Administer User Accounts : NO"
    )

    logger.info(
        "  Remote Console Access    : YES"
    )

    logger.info(
        "  Virtual Power and Reset  : YES"
    )

    logger.info(
        "  Virtual Media            : YES"
    )

    logger.info(
        "  Configure iLO Settings   : NO"
    )

    logger.info(
        ""
    )

    logger.info(
        "HPONCFG timeout : %s seconds",
        COMMAND_TIMEOUT
    )

    logger.info(
        "Quiet time      : %s seconds",
        COMMAND_QUIET_TIME
    )

    logger.info(
        "HPONCFG delay   : %s seconds",
        HPONCFG_LINE_DELAY
    )

    logger.info(
        ""
    )

    active_oa = None

    results = []

    try:

        # ==================================================================
        # STEP 1 - FIND ACTIVE OA
        # ==================================================================

        active_oa, active_ip, active_bay = (
            find_active_oa()
        )

        if active_oa is None:

            raise RuntimeError(
                "Could not find an ACTIVE OA."
            )

        logger.info(
            ""
        )

        logger.info(
            "Using ACTIVE OA%d: %s",
            active_bay,
            active_ip
        )

        # ==================================================================
        # STEP 2 - DISCOVER BLADES
        # ==================================================================

        blades = discover_blades(
            active_oa
        )

        if not blades:

            raise RuntimeError(
                "No blade servers discovered."
            )

        # ==================================================================
        # IMPORTANT:
        #
        # The discovery connection is no longer needed by the worker
        # threads. Close it before starting parallel HPONCFG operations.
        # ==================================================================

        active_oa.close()

        active_oa = None

        logger.info(
            ""
        )

        logger.info(
            "Starting parallel processing..."
        )

        logger.info(
            "Workers: %d",
            MAX_WORKERS
        )

        logger.info(
            "Blades : %d",
            len(blades)
        )

        logger.info(
            ""
        )

        # ==================================================================
        # STEP 3 - PARALLEL PROCESSING
        # ==================================================================

        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:

            future_to_blade = {}

            for blade in blades:

                future = executor.submit(
                    process_blade,
                    active_ip,
                    blade
                )

                future_to_blade[
                    future
                ] = blade

            # --------------------------------------------------------------
            # Collect results as each blade completes.
            # --------------------------------------------------------------

            for future in as_completed(
                future_to_blade
            ):

                blade = future_to_blade[
                    future
                ]

                slot = blade["slot"]

                try:

                    result = future.result()

                except Exception as exc:

                    logger.exception(
                        "[Slot %02d] Future failed: %s",
                        slot,
                        exc
                    )

                    result = {
                        "slot": slot,
                        "ilo_name": blade[
                            "ilo_name"
                        ],
                        "ilo_ip": blade[
                            "ilo_ip"
                        ],
                        "status": "ERROR",
                        "message": str(exc),
                    }

                results.append(
                    result
                )

                # ----------------------------------------------------------
                # Immediate completion message.
                # ----------------------------------------------------------

                logger.info(
                    ""
                )

                logger.info(
                    "[Slot %02d] THREAD COMPLETED -> %s",
                    slot,
                    result["status"]
                )

        # ==================================================================
        # STEP 4 - FINAL REPORT
        # ==================================================================

        success = print_final_report(
            results
        )

        elapsed = (
            time.time()
            - start_time
        )

        logger.info(
            "Total execution time: %.1f seconds",
            elapsed
        )

        if success:

            logger.info(
                "ALL BLADES COMPLETED SUCCESSFULLY."
            )

            return 0

        logger.error(
            "ONE OR MORE BLADES FAILED."
        )

        return 1

    except Exception as exc:

        logger.exception(
            "FATAL ERROR: %s",
            exc
        )

        return 1

    finally:

        if active_oa:

            try:

                active_oa.close()

            except Exception:

                pass

            logger.info(
                "ACTIVE OA connection closed."
            )


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )