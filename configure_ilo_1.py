#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import time
import socket
import warnings
from pathlib import Path

warnings.filterwarnings(
    "ignore",
    message=".*Python 3.6 is no longer supported.*"
)

warnings.filterwarnings("ignore", module="cryptography")
warnings.filterwarnings("ignore", module="paramiko")

import paramiko
import pandas as pd

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined
)


# =============================================================================
#                               CREDENTIALS
# =============================================================================

OA_USERNAME = "Administrator"
OA_PASSWORD = "Th@les01"

ILO_LOGIN = "admin"
ILO_PASSWORD = "password"

ILO_ADVANCED_LICENSE_KEY = "35SCR-RYLML-CBK7N-TD3B9-GGBW2"

FENCE_USER_NAME = "Pacemaker Fence"
FENCE_USER_LOGIN = "hpilofence"
FENCE_USER_PASSWORD = "Th@les01"

IPMI_PORT = "623"

ILO_DOMAIN = "mak.iss"

DIR_USER_CONTEXT_1 = "OU=IT,OU=ISS,DC=mak,DC=iss"
DIR_USER_CONTEXT_2 = "CN=Users,DC=mak,DC=iss"
DIR_USER_CONTEXT_3 = "CN=Builtin,DC=mak,DC=iss"
DIR_USER_CONTEXT_4 = "@mak.iss"


# =============================================================================
#                               SCOPE SETTINGS
# =============================================================================

SCOPE_SETTINGS = {

    "SIL": {
        "PRIMARY_DNS": "10.130.2.11",
        "SECONDARY_DNS": "10.130.2.12",
        "DIRECTORY_SERVER": "INFCOSADU001MP.mak.iss"
    },

    "MTR": {
        "PRIMARY_DNS": "10.130.2.11",
        "SECONDARY_DNS": "10.130.2.12",
        "DIRECTORY_SERVER": "INFCOSADU001MP.mak.iss"
    },

    "RTR": {
        "PRIMARY_DNS": "10.130.3.11",
        "SECONDARY_DNS": "10.130.3.12",
        "DIRECTORY_SERVER": "INFCOSADU002MP.mak.iss"
    }
}


# =============================================================================
#                               SETTINGS
# =============================================================================

DEBUG_MODE = False
SSH_PORT = 22
SSH_CONNECT_TIMEOUT = 30
COMMAND_TIMEOUT = 600
SSH_KEEPALIVE_INTERVAL = 5
SSH_READ_INTERVAL = 0.1
HPONCFG_LINE_DELAY = 0.05
STATUS_INTERVAL = 30
OA_STATUS_TIMEOUT = 15

# =============================================================================
#                               PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "Templates"
TEMPLATE_FILE = "ilo_config.xml.j2"
EXCEL_FILE = TEMPLATE_DIR / "Resource List-v7.6.xlsx"

# =============================================================================
#                               UTILITIES
# =============================================================================

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def debug(message):
    if DEBUG_MODE:
        print(
            "[{}] [DEBUG] {}".format(
                timestamp(),
                message
            )
        )


# =============================================================================
#                               JINJA
# =============================================================================

def create_jinja_environment():

    return Environment(
        loader=FileSystemLoader(
            str(TEMPLATE_DIR)
        ),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True
    )


def render_template(
        add_user,
        apply_ipmi_config,
        apply_license,
        scope_data,
        server_name,
        server_fqdn):

    env = create_jinja_environment()

    template = env.get_template(
        TEMPLATE_FILE
    )

    return template.render(

        apply_license=apply_license,

        ilo_license_key=ILO_ADVANCED_LICENSE_KEY,

        add_user=add_user,

        apply_ipmi_config=apply_ipmi_config,

        ilo_login=ILO_LOGIN,
        ilo_password=ILO_PASSWORD,

        fence_user_name=FENCE_USER_NAME,
        fence_user_login=FENCE_USER_LOGIN,
        fence_user_password=FENCE_USER_PASSWORD,

        ipmi_port=IPMI_PORT,

        server_name=server_name,
        server_fqdn=server_fqdn,

        ilo_domain=ILO_DOMAIN,

        primary_dns=scope_data["PRIMARY_DNS"],
        secondary_dns=scope_data["SECONDARY_DNS"],

        directory_server=scope_data["DIRECTORY_SERVER"],

        dir_user_context_1=DIR_USER_CONTEXT_1,
        dir_user_context_2=DIR_USER_CONTEXT_2,
        dir_user_context_3=DIR_USER_CONTEXT_3,
        dir_user_context_4=DIR_USER_CONTEXT_4
    )


# =============================================================================
#                           OA SSH CONNECTION
# =============================================================================

class OAConnection(object):

    def __init__(
            self,
            username,
            password,
            port=22):

        self.hostname = None

        self.username = username
        self.password = password
        self.port = port

        self.client = None
        self.channel = None


    # -------------------------------------------------------------------------
    # CONNECT
    # -------------------------------------------------------------------------

    def connect(self, hostname):

        self.hostname = hostname

        debug(
            "Connecting to OA {}:{}"
            .format(
                hostname,
                self.port
            )
        )

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

            allow_agent=False
        )

        transport = self.client.get_transport()

        if not transport:

            raise RuntimeError(
                "Could not obtain SSH transport."
            )

        if not transport.is_active():

            raise RuntimeError(
                "SSH transport is not active."
            )

        transport.set_keepalive(
            SSH_KEEPALIVE_INTERVAL
        )

        try:

            sock = transport.sock

            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_KEEPALIVE,
                1
            )

            debug(
                "TCP keepalive enabled."
            )

        except Exception as exc:

            debug(
                "Could not configure TCP keepalive: {}"
                .format(exc)
            )

        self.channel = self.client.invoke_shell()

        debug(
            "Interactive OA shell opened."
        )

        time.sleep(1)

        initial_output = self._drain_channel()

        if initial_output:

            debug(
                "Initial OA shell output:"
            )

            if DEBUG_MODE:

                print(
                    "\n----- OA INITIAL OUTPUT -----"
                )

                print(initial_output)

                print(
                    "-----------------------------\n"
                )


    # -------------------------------------------------------------------------
    # CLOSE
    # -------------------------------------------------------------------------

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


    # -------------------------------------------------------------------------
    # CHECK CONNECTION
    # -------------------------------------------------------------------------

    def is_connected(self):

        if not self.client:

            return False

        transport = self.client.get_transport()

        if not transport:

            return False

        return transport.is_active()


    # -------------------------------------------------------------------------
    # DRAIN CHANNEL
    # -------------------------------------------------------------------------

    def _drain_channel(self):

        if not self.channel:

            return ""

        output = ""

        while self.channel.recv_ready():

            try:

                data = self.channel.recv(
                    65535
                )

            except Exception as exc:

                debug(
                    "Error draining SSH channel: {}"
                    .format(exc)
                )

                break

            if not data:

                break

            output += data.decode(
                "utf-8",
                errors="replace"
            )

        return output


    # -------------------------------------------------------------------------
    # EXECUTE NORMAL OA CLI COMMAND
    # -------------------------------------------------------------------------

    def execute_oa_command(
            self,
            command,
            timeout=OA_STATUS_TIMEOUT):

        if not self.channel:

            raise RuntimeError(
                "SSH channel is not available."
            )

        # Clear old data first
        stale_output = self._drain_channel()

        if stale_output:

            debug(
                "Discarded stale OA output before command."
            )

        debug(
            "Executing OA command: {}"
            .format(command)
        )

        self.channel.send(
            command + "\n"
        )

        output = ""

        start_time = time.monotonic()

        deadline = (
            start_time + timeout
        )

        last_data_time = time.monotonic()

        while time.monotonic() < deadline:

            if self.channel.closed:

                break

            if self.channel.recv_ready():

                data = self.channel.recv(
                    65535
                )

                if not data:

                    break

                decoded = data.decode(
                    "utf-8",
                    errors="replace"
                )

                output += decoded

                last_data_time = time.monotonic()

                # OA prompt normally ends with >
                #
                # We wait briefly after receiving data to allow
                # complete command output to arrive.

                time.sleep(0.2)

                if not self.channel.recv_ready():

                    break

            else:

                if (
                    time.monotonic()
                    - last_data_time
                    >= 1.0
                ) and output:

                    break

                time.sleep(
                    SSH_READ_INTERVAL
                )

        debug(
            "OA command completed."
        )

        if DEBUG_MODE:

            print(
                "\n----- OA COMMAND OUTPUT -----"
            )

            print(output)

            print(
                "-----------------------------\n"
            )

        return output


    # -------------------------------------------------------------------------
    # CHECK OA ROLE
    #
    # Returns:
    #
    #   ACTIVE
    #   STANDBY
    #   UNKNOWN
    # -------------------------------------------------------------------------

    def get_oa_role(self):

        print(
            "  -> Checking OA status..."
        )

        output = self.execute_oa_command(
            "SHOW OA STATUS",
            timeout=OA_STATUS_TIMEOUT
        )

        output_lower = output.lower()

        # Check explicitly for standby first.
        # This is important because some OA status output may contain
        # both OA controllers in the same response.

        if "standby" in output_lower:

            # Try to identify whether the current OA itself is standby.
            #
            # Common outputs contain information such as:
            #
            # OA Status: Standby
            #
            # or:
            #
            # Active OA: 1
            # This OA: Standby

            if re.search(
                    r'(this\s+oa|local\s+oa|oa\s+status|status)'
                    r'.{0,50}standby',
                    output_lower,
                    re.IGNORECASE | re.DOTALL):

                return "STANDBY"

        if "active" in output_lower:

            if re.search(
                    r'(this\s+oa|local\s+oa|oa\s+status|status)'
                    r'.{0,50}active',
                    output_lower,
                    re.IGNORECASE | re.DOTALL):

                return "ACTIVE"

        # Fallback logic
        #
        # If the output clearly contains standby but not active,
        # treat it as standby.

        if (
                "standby" in output_lower
                and "active" not in output_lower):

            return "STANDBY"

        # If it clearly contains active but not standby,
        # treat it as active.

        if (
                "active" in output_lower
                and "standby" not in output_lower):

            return "ACTIVE"

        return "UNKNOWN"


    # -------------------------------------------------------------------------
    # READ HPONCFG OUTPUT
    # -------------------------------------------------------------------------

    def read_command_output(
            self,
            timeout=COMMAND_TIMEOUT):

        if not self.channel:

            raise RuntimeError(
                "SSH channel is not available."
            )

        output = ""

        start_time = time.monotonic()

        deadline = (
            start_time + timeout
        )

        last_status_report = 0

        debug(
            "Waiting for OA output. "
            "Timeout: {} seconds."
            .format(timeout)
        )

        while time.monotonic() < deadline:

            if self.channel.closed:

                debug(
                    "SSH channel closed while waiting "
                    "for OA response."
                )

                break

            if self.channel.recv_ready():

                try:

                    data = self.channel.recv(
                        65535
                    )

                except Exception as exc:

                    raise RuntimeError(
                        "Failed receiving OA output: {}"
                        .format(exc)
                    )

                if not data:

                    debug(
                        "Received empty SSH data block."
                    )

                    break

                decoded = data.decode(
                    "utf-8",
                    errors="replace"
                )

                output += decoded

                debug(
                    "Received {} bytes from OA."
                    .format(
                        len(data)
                    )
                )

                if DEBUG_MODE:

                    print()

                    print(
                        "----- OA OUTPUT START -----"
                    )

                    print(decoded)

                    print(
                        "----- OA OUTPUT END -------"
                    )

                    print()

                if "END RIBCL RESULTS" in output:

                    debug(
                        "Detected END RIBCL RESULTS."
                    )

                    time.sleep(0.5)

                    extra_output = (
                        self._drain_channel()
                    )

                    if extra_output:

                        output += extra_output

                    return output

            else:

                elapsed = int(
                    time.monotonic()
                    - start_time
                )

                if (
                    elapsed >=
                    last_status_report
                    + STATUS_INTERVAL
                ):

                    last_status_report = elapsed

                    debug(
                        "Still waiting for OA output. "
                        "Elapsed: {} seconds."
                        .format(elapsed)
                    )

                time.sleep(
                    SSH_READ_INTERVAL
                )

        debug(
            "COMMAND_TIMEOUT reached."
        )

        return output


    # -------------------------------------------------------------------------
    # EXECUTE HPONCFG
    # -------------------------------------------------------------------------

    def execute_hponcfg(
            self,
            bay_number,
            ribcl,
            end_marker="ILO_RIBCL_EOF"):

        if not self.is_connected():

            raise RuntimeError(
                "SSH connection to OA is no longer active."
            )

        if not self.channel:

            raise RuntimeError(
                "OA SSH channel is not available."
            )

        stale_output = self._drain_channel()

        if stale_output:

            debug(
                "Discarding stale OA output."
            )

        command = (
            "HPONCFG {0} << {1}\n"
            "{2}\n"
            "{1}\n"
        ).format(
            bay_number,
            end_marker,
            ribcl.rstrip()
        )

        lines = command.splitlines()

        total_lines = len(lines)

        debug(
            "Sending HPONCFG command "
            "line by line. Total lines: {}"
            .format(total_lines)
        )

        for line_number, line in enumerate(
                lines,
                1):

            if self.channel.closed:

                raise RuntimeError(
                    "SSH channel closed while sending "
                    "HPONCFG command."
                )

            try:

                self.channel.send(
                    line + "\n"
                )

            except Exception as exc:

                raise RuntimeError(
                    "Failed sending HPONCFG line {}: {}"
                    .format(
                        line_number,
                        exc
                    )
                )

            debug(
                "Sent line {}/{}"
                .format(
                    line_number,
                    total_lines
                )
            )

            time.sleep(
                HPONCFG_LINE_DELAY
            )

        debug(
            "All HPONCFG lines sent."
        )

        return self.read_command_output(
            timeout=COMMAND_TIMEOUT
        )


# =============================================================================
#                           iLO CHECK FUNCTIONS
# =============================================================================

def check_ilo_license(
        oa,
        bay_number):

    print(
        "  -> Checking current iLO License status..."
    )

    ribcl = (
        '<RIBCL VERSION="2.0">\n'
        '<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n'
        '<RIB_INFO MODE="read">\n'
        '<GET_ALL_LICENSES/>\n'
        '</RIB_INFO>\n'
        '</LOGIN>\n'
        '</RIBCL>'
    ).format(
        ILO_LOGIN,
        ILO_PASSWORD
    )

    output = oa.execute_hponcfg(
        bay_number=bay_number,
        ribcl=ribcl,
        end_marker="ILO_LICENSE_CHECK_EOF"
    )

    if "END RIBCL RESULTS" not in output:

        raise RuntimeError(
            "OA did not complete "
            "the iLO license check."
        )

    match = re.search(
        r'LICENSE_TYPE\s*VALUE\s*=\s*["\']([^"\']+)["\']',
        output,
        re.IGNORECASE
    )

    if match:

        license_type = match.group(1)

        print(
            "  -> Detected License: {}"
            .format(license_type)
        )

        if "advanced" in license_type.lower():

            print(
                "  -> iLO Advanced features "
                "already enabled."
            )

            return False

    print(
        "  -> iLO Advanced features NOT found "
        "or undetermined. Queuing license activation."
    )

    return True


def check_fence_user(
        oa,
        bay_number):

    print(
        "  -> Checking if user '{}' exists..."
        .format(FENCE_USER_LOGIN)
    )

    ribcl = (
        '<RIBCL VERSION="2.0">\n'
        '<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n'
        '<USER_INFO MODE="read">\n'
        '<GET_USER USER_LOGIN="{2}"/>\n'
        '</USER_INFO>\n'
        '</LOGIN>\n'
        '</RIBCL>'
    ).format(
        ILO_LOGIN,
        ILO_PASSWORD,
        FENCE_USER_LOGIN
    )

    output = oa.execute_hponcfg(
        bay_number=bay_number,
        ribcl=ribcl,
        end_marker="ILO_USER_CHECK_EOF"
    )

    if "END RIBCL RESULTS" not in output:

        raise RuntimeError(
            "OA did not complete "
            "the fence user check."
        )

    statuses = re.findall(
        r'<RESPONSE\s+STATUS=["\']([^"\']+)["\']',
        output,
        re.IGNORECASE
    )

    if "0x0000" in statuses:

        return True

    return False


def check_ipmi_settings(
        oa,
        bay_number):

    print(
        "  -> Checking current IPMI settings..."
    )

    ribcl = (
        '<RIBCL VERSION="2.0">\n'
        '<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n'
        '<RIB_INFO MODE="read">\n'
        '<GET_GLOBAL_SETTINGS/>\n'
        '</RIB_INFO>\n'
        '</LOGIN>\n'
        '</RIBCL>'
    ).format(
        ILO_LOGIN,
        ILO_PASSWORD
    )

    output = oa.execute_hponcfg(
        bay_number=bay_number,
        ribcl=ribcl,
        end_marker="ILO_IPMI_CHECK_EOF"
    )

    if "END RIBCL RESULTS" not in output:

        raise RuntimeError(
            "OA did not complete "
            "the IPMI settings check."
        )

    port_match = re.search(
        r'IPMI_DCMI_OVER_LAN_PORT.*?VALUE=["\'](\d+)["\']',
        output,
        re.IGNORECASE
    )

    enabled_match = re.search(
        r'IPMI_DCMI_OVER_LAN_ENABLED.*?VALUE=["\']([Yy])["\']',
        output,
        re.IGNORECASE
    )

    port_ok = bool(
        port_match
        and port_match.group(1) == str(IPMI_PORT)
    )

    enabled = bool(enabled_match)

    if enabled and port_ok:

        print(
            "  -> IPMI already configured correctly."
        )

        return False

    print(
        "  -> IPMI needs configuration. "
        "Queuing global settings update."
    )

    return True


# =============================================================================
#                           VALIDATE RESULT
# =============================================================================

def validate_hponcfg_result(output):

    if "END RIBCL RESULTS" not in output:

        print(
            "\n  [ERROR] OA did not return "
            "'END RIBCL RESULTS'."
        )

        if output:

            print(
                "\n----- PARTIAL OA OUTPUT -----"
            )

            print(output)

            print(
                "-----------------------------"
            )

        return False

    responses = re.findall(
        r'<RESPONSE\s+STATUS=["\']([^"\']+)["\']'
        r'\s+MESSAGE=["\']([^"\']+)["\']',
        output,
        re.IGNORECASE
    )

    has_error = False

    for status, message in responses:

        if status != "0x0000":

            print(
                "  [ERROR] iLO response: "
                "STATUS={} | MESSAGE='{}'"
                .format(
                    status,
                    message
                )
            )

            has_error = True

    if has_error:

        return False

    print(
        "  [SUCCESS] Configuration applied."
    )

    return True


# =============================================================================
#                               MAIN
# =============================================================================

def main():

    if not EXCEL_FILE.is_file():

        print(
            "ERROR: Excel inventory file missing: {}"
            .format(EXCEL_FILE),
            file=sys.stderr
        )

        return 1


    enclosure_input = input(
        "Enter Enclosure Name: "
    ).strip()

    if not enclosure_input:

        print(
            "ERROR: Enclosure name cannot be empty."
        )

        return 1


    print(
        "\nLoading inventory from '{}'..."
        .format(EXCEL_FILE)
    )

    try:

        df = pd.read_excel(
            EXCEL_FILE,
            sheet_name="General Resource List",
            engine="openpyxl"
        )

        df.columns = [
            str(column).strip().lower()
            for column in df.columns
        ]

    except Exception as exc:

        print(
            "ERROR: Failed reading inventory: {}"
            .format(exc)
        )

        return 1


    # -------------------------------------------------------------------------
    # FIND ENCLOSURE
    # -------------------------------------------------------------------------

    enc_df = df[
        df["enclosure_physical_name"]
        .astype(str)
        .str.strip()
        == enclosure_input
    ]

    if enc_df.empty:

        print(
            "ERROR: Enclosure '{}' not found."
            .format(enclosure_input)
        )

        return 1


    # -------------------------------------------------------------------------
    # FIND BOTH OA CONTROLLERS
    #
    # Excel example:
    #
    # equipment_physical_name       enclosure_slot     ilo_ip
    #
    # SV-MTR-0303-11O-01           01                 10.101.18.35
    # SV-MTR-0303-11O-02           02                 10.101.18.36
    # -------------------------------------------------------------------------

    oa_df = enc_df[
        enc_df["equipment_type"]
        .astype(str)
        .str.strip()
        == "Enclosure OA"
    ].copy()

    if oa_df.empty:

        print(
            "ERROR: No OA controllers found "
            "for enclosure '{}'."
            .format(enclosure_input)
        )

        return 1


    oa_controllers = []

    for _, row in oa_df.iterrows():

        oa_name = str(
            row.get(
                "equipment_physical_name",
                ""
            )
        ).strip()

        oa_ip = row.get(
            "ilo_ip"
        )

        oa_slot = row.get(
            "enclosure_slot"
        )

        if pd.isna(oa_ip):

            continue

        oa_ip = str(
            oa_ip
        ).strip()

        try:

            oa_slot_number = int(
                float(oa_slot)
            )

        except Exception:

            oa_slot_number = 999

        oa_controllers.append({

            "name": oa_name,

            "ip": oa_ip,

            "slot": oa_slot_number
        })


    # Sort OA-01 before OA-02
    oa_controllers.sort(
        key=lambda item: item["slot"]
    )


    if not oa_controllers:

        print(
            "ERROR: No valid OA IP addresses found."
        )

        return 1


    print(
        "\nFound {} OA controller(s):"
        .format(
            len(oa_controllers)
        )
    )

    for oa_info in oa_controllers:

        print(
            "  OA Slot {} | {} | {}"
            .format(
                oa_info["slot"],
                oa_info["name"],
                oa_info["ip"]
            )
        )


    # -------------------------------------------------------------------------
    # CONNECT TO ACTIVE OA
    # -------------------------------------------------------------------------

    oa = None

    active_oa_found = False

    for oa_info in oa_controllers:

        oa_ip = oa_info["ip"]

        oa_name = oa_info["name"]

        print(
            "\nAttempting to connect to OA: {} ({})..."
            .format(
                oa_name,
                oa_ip
            )
        )

        current_oa = OAConnection(

            OA_USERNAME,

            OA_PASSWORD,

            SSH_PORT
        )

        try:

            current_oa.connect(
                oa_ip
            )

            print(
                "SUCCESS: Connected to OA {}."
                .format(
                    oa_ip
                )
            )


            # -------------------------------------------------------------
            # CHECK ACTIVE / STANDBY ROLE
            # -------------------------------------------------------------

            oa_role = current_oa.get_oa_role()

            print(
                "  -> OA role detected: {}"
                .format(
                    oa_role
                )
            )


            if oa_role == "ACTIVE":

                print(
                    "SUCCESS: This is the ACTIVE OA. "
                    "Using {} ({}) for configuration."
                    .format(
                        oa_name,
                        oa_ip
                    )
                )

                oa = current_oa

                active_oa_found = True

                break


            elif oa_role == "STANDBY":

                print(
                    "  -> This OA is STANDBY. "
                    "Disconnecting and trying the next OA..."
                )

                current_oa.close()

                continue


            else:

                print(
                    "WARNING: Could not determine "
                    "whether OA {} is ACTIVE or STANDBY."
                    .format(
                        oa_ip
                    )
                )

                print(
                    "Disconnecting and trying next OA..."
                )

                current_oa.close()

                continue


        except Exception as exc:

            print(
                "WARNING: Failed while connecting/checking "
                "OA {}: {}"
                .format(
                    oa_ip,
                    exc
                )
            )

            current_oa.close()


    if not active_oa_found:

        print(
            "\nERROR: Could not find an ACTIVE OA controller."
        )

        return 1


    # -------------------------------------------------------------------------
    # FIND BLADE SERVERS
    # -------------------------------------------------------------------------

    blade_df = enc_df[
        enc_df["equipment_type"]
        .astype(str)
        .str.contains(
            "Blade Server",
            case=False,
            na=False
        )
    ]


    print(
        "\nFound {} Blade Server(s) "
        "in enclosure '{}'. Beginning configuration...\n"
        .format(
            len(blade_df),
            enclosure_input
        )
    )


    # -------------------------------------------------------------------------
    # PROCESS BLADES
    # -------------------------------------------------------------------------

    try:

        for _, row in blade_df.iterrows():

            print(
                "-" * 78
            )

            try:

                bay_number = int(
                    float(
                        row["enclosure_slot"]
                    )
                )

            except Exception:

                print(
                    "WARNING: Invalid bay number. Skipping."
                )

                continue


            scope = str(
                row.get(
                    "scope",
                    ""
                )
            ).strip().upper()


            server_name = str(
                row.get(
                    "hostname",
                    ""
                )
            ).strip()


            server_fqdn = str(
                row.get(
                    "ilo_hostname",
                    ""
                )
            ).strip()


            if scope not in SCOPE_SETTINGS:

                print(
                    "WARNING: Unknown scope '{}'. "
                    "Skipping Bay {}."
                    .format(
                        scope,
                        bay_number
                    )
                )

                continue


            print(
                "Configuring Bay {} | "
                "Server: {} | "
                "Scope: {}"
                .format(
                    bay_number,
                    server_name,
                    scope
                )
            )


            scope_data = SCOPE_SETTINGS[
                scope
            ]


            # -------------------------------------------------------------
            # CHECK LICENSE
            # -------------------------------------------------------------

            apply_license = check_ilo_license(
                oa,
                bay_number
            )


            # -------------------------------------------------------------
            # CHECK FENCE USER
            # -------------------------------------------------------------

            user_exists = check_fence_user(
                oa,
                bay_number
            )

            if user_exists:

                print(
                    "  -> User '{}' exists. "
                    "Skipping creation."
                    .format(
                        FENCE_USER_LOGIN
                    )
                )

            else:

                print(
                    "  -> User '{}' missing. "
                    "Queuing creation."
                    .format(
                        FENCE_USER_LOGIN
                    )
                )


            # -------------------------------------------------------------
            # CHECK IPMI
            # -------------------------------------------------------------

            apply_ipmi = check_ipmi_settings(
                oa,
                bay_number
            )


            # -------------------------------------------------------------
            # RENDER RIBCL
            # -------------------------------------------------------------

            ribcl = render_template(

                add_user=not user_exists,

                apply_ipmi_config=apply_ipmi,

                apply_license=apply_license,

                scope_data=scope_data,

                server_name=server_name,

                server_fqdn=server_fqdn
            )


            # -------------------------------------------------------------
            # PUSH CONFIGURATION
            # -------------------------------------------------------------

            print(
                "  -> Pushing RIBCL configuration..."
            )

            result = oa.execute_hponcfg(
                bay_number,
                ribcl
            )


            # -------------------------------------------------------------
            # VALIDATE RESULT
            # -------------------------------------------------------------

            validate_hponcfg_result(
                result
            )


    except KeyboardInterrupt:

        print(
            "\nExecution interrupted by user."
        )

        return 1


    except Exception as exc:

        print(
            "\nERROR: {}"
            .format(exc),
            file=sys.stderr
        )

        return 1


    finally:

        if oa:

            oa.close()


        print(
            "\n" + "=" * 78
        )

        print(
            "Script execution completed."
        )

        print(
            "=" * 78
        )


    return 0


# =============================================================================
#                               ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )