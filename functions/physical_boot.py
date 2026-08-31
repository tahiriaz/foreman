# BUILD_MARKER: FOREMAN_PHYSICAL_NETWORK_BOOT_V4_CRYPTO_CLEAN_20260830

import re
import socket
import threading
import time
import warnings
from xml.sax.saxutils import quoteattr

import openpyxl
import requests
import urllib3

from functions import vars


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


RACK_TYPES = set(
    vars.FOREMAN_PHYSICAL_NETWORK_BOOT_RACK_TYPES
)

BLADE_TYPES = set(
    vars.FOREMAN_PHYSICAL_NETWORK_BOOT_BLADE_TYPES
)

PRINT_LOCK = threading.Lock()
OA_CACHE_LOCK = threading.Lock()
OA_INVENTORY_CACHE = None

OA_OPERATION_LOCK_GUARD = threading.Lock()
OA_OPERATION_LOCKS = {}

PARAMIKO_IMPORT_LOCK = threading.Lock()
PARAMIKO_MODULE = None


class IloUnreachableError(Exception):
    """Raised only when the iLO network endpoint cannot be reached."""


class IloAuthenticationError(Exception):
    """Raised when iLO is reachable but the configured credentials fail."""


class IloRedfishTransportError(Exception):
    """
    iLO TCP/443 is reachable, but the Redfish HTTP transaction repeatedly
    failed. This is not an "iLO unreachable" condition and must not trigger OA.
    """


def _log(host, message):

    row = host.get(
        "_excel_row",
        "-",
    )

    name = str(
        host.get(
            "hostname",
            host.get(
                "logical_name",
                "Unknown",
            ),
        )
    ).strip()

    ip = str(
        host.get(
            "ilo_ip",
            "",
        )
        or ""
    ).strip()

    target = (
        ip
        if ip
        else name
    )

    with PRINT_LOCK:

        print(
            "[PXE | Row {} | {} | {}] {}".format(
                row,
                name,
                target,
                message,
            ),
            flush=True,
        )


def _normalize_equipment_type(host):

    return str(
        host.get(
            "equipment_type",
            "",
        )
        or ""
    ).strip()


def is_supported_physical_host(host):

    equipment_type = (
        _normalize_equipment_type(
            host
        )
    )

    return (
        equipment_type in RACK_TYPES
        or equipment_type in BLADE_TYPES
    )


def configure_next_network_boot(host):
    """
    Configure one-time network/PXE boot for a physical host.

    Rack mount:
      - connect directly to iLO Redfish.

    Blade:
      - try direct iLO Redfish first;
      - only when iLO is NETWORK-UNREACHABLE, discover the ACTIVE OA and use
        HPONCFG/RIBCL through the enclosure.

    For direct iLO, a host already in POST is ForceOff, PXE-once is configured
    while powered off, and the host is powered on again. A normally-running
    host is rebooted after PXE/Once verification; an Off host is powered on.
    Therefore successful PXE configuration always starts installation
    immediately.

    Existing Foreman host handling is intentionally outside this module:
    process_host.py calls this only for a newly-created Foreman host.
    """
    equipment_type = (
        _normalize_equipment_type(
            host
        )
    )

    if not (
        vars.FOREMAN_PHYSICAL_NETWORK_BOOT_ENABLED
    ):

        return {
            "success":
                True,

            "status":
                "Disabled",

            "method":
                "Disabled",

            "details":
                (
                    "Physical-host next-boot network/PXE "
                    "configuration is disabled in vars.py"
                ),
        }

    if equipment_type in BLADE_TYPES:

        return (
            _configure_blade(
                host
            )
        )

    if equipment_type in RACK_TYPES:

        return (
            _configure_direct_ilo(
                host,
                vars.ILO_RM_USERNAME,
                vars.ILO_RM_PASSWORD,
                allow_oa_fallback=False,
            )
        )

    return {
        "success":
            True,

        "status":
            "Skipped",

        "method":
            "N/A",

        "details":
            (
                "Equipment type '{}' is not configured "
                "for physical-host PXE boot."
            ).format(
                equipment_type
            ),
    }


def _load_paramiko():
    """
    Import Paramiko only when ACTIVE OA fallback is actually required.

    The project intentionally runs on Python 3.6. The installed cryptography
    package emits deprecation warnings at import time because Python 3.6 is
    end-of-life. Those messages do not indicate an SSH/OA failure.

    Warning suppression is narrowly scoped to the Paramiko import and only
    known cryptography deprecation messages are hidden. Runtime SSH exceptions
    and unrelated warnings remain visible.
    """

    global PARAMIKO_MODULE

    if PARAMIKO_MODULE is not None:

        return PARAMIKO_MODULE

    with PARAMIKO_IMPORT_LOCK:

        if PARAMIKO_MODULE is not None:

            return PARAMIKO_MODULE

        if (
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_SUPPRESS_CRYPTO_DEPRECATION_WARNINGS
        ):

            with warnings.catch_warnings():

                warnings.filterwarnings(
                    "ignore",
                    message=(
                        r"Python 3\.6 is no longer supported by "
                        r"the Python core team\..*"
                    ),
                )

                warnings.filterwarnings(
                    "ignore",
                    message=r".*Blowfish has been deprecated.*",
                )

                warnings.filterwarnings(
                    "ignore",
                    message=(
                        r".*TripleDES has been moved to "
                        r"cryptography\.hazmat\.decrepit.*"
                    ),
                )

                import paramiko as imported_paramiko

        else:

            import paramiko as imported_paramiko

        PARAMIKO_MODULE = (
            imported_paramiko
        )

        return PARAMIKO_MODULE


def _get_oa_operation_lock(
    host,
):

    if not (
        vars
        .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_SERIALIZE_PER_ENCLOSURE
    ):

        return threading.Lock()

    enclosure_name = str(
        host.get(
            "enclosure_physical_name",
            "",
        )
        or ""
    ).strip().lower()

    key = (
        enclosure_name
        if enclosure_name
        else "__unknown_enclosure__"
    )

    with OA_OPERATION_LOCK_GUARD:

        lock = (
            OA_OPERATION_LOCKS.get(
                key
            )
        )

        if lock is None:

            lock = threading.Lock()

            OA_OPERATION_LOCKS[
                key
            ] = lock

        return lock


# =============================================================================
# DIRECT iLO REDFISH
# =============================================================================

class RedfishBootClient(object):

    def __init__(
        self,
        host,
        username,
        password,
    ):

        self.host = host
        self.ip = str(
            host.get(
                "ilo_ip",
                "",
            )
            or ""
        ).strip()

        self.username = username
        self.password = password

        self.base_url = (
            "https://{}".format(
                self.ip
            )
            if self.ip
            else ""
        )

        self.system_uri = None

        self.session = (
            requests.Session()
        )

        self.session.auth = (
            self.username,
            self.password,
        )

        self.session.verify = (
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_VERIFY_ILO_SSL
        )

        self.session.headers.update({
            "Accept":
                "application/json",

            "Content-Type":
                "application/json",

            "Connection":
                "close",
        })


    def close(self):

        try:
            self.session.close()
        except Exception:
            pass


    def _timeout(self):

        return (
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_CONNECT_TIMEOUT_SECONDS,
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_REQUEST_TIMEOUT_SECONDS,
        )


    def _tcp_443_reachable(self):

        attempts = max(
            1,
            int(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_TCP_PROBE_RETRIES
            ),
        )

        for attempt in range(
            1,
            attempts + 1,
        ):

            sock = None

            try:

                sock = socket.create_connection(
                    (
                        self.ip,
                        443,
                    ),
                    timeout=(
                        vars
                        .FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_TCP_PROBE_TIMEOUT_SECONDS
                    ),
                )

                return True

            except (
                socket.error,
                OSError,
            ):

                if attempt < attempts:

                    time.sleep(
                        vars
                        .FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_RETRY_DELAY_SECONDS
                    )

            finally:

                if sock:

                    try:
                        sock.close()
                    except Exception:
                        pass

        return False


    @staticmethod
    def _request_can_retry(
        method,
    ):

        # PATCH of Pxe/Once is safe to repeat. Do not automatically repeat POST
        # power actions because a duplicate ForceRestart could cause 2 reboots.
        return (
            str(
                method
            ).upper()
            in (
                "GET",
                "HEAD",
                "OPTIONS",
                "PATCH",
            )
        )


    def _new_http_session(self):

        try:
            self.session.close()
        except Exception:
            pass

        self.session = requests.Session()

        self.session.auth = (
            self.username,
            self.password,
        )

        self.session.verify = (
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_VERIFY_ILO_SSL
        )

        self.session.headers.update({
            "Accept":
                "application/json",

            "Content-Type":
                "application/json",

            # iLO 4 can close persistent HTTP connections. Do not reuse a
            # connection that the management processor may already have closed.
            "Connection":
                "close",
        })


    def request(
        self,
        method,
        uri,
        **kwargs
    ):

        if not self.base_url:

            raise IloUnreachableError(
                "iLO IP address is missing"
            )

        if uri.startswith(
            "http://"
        ) or uri.startswith(
            "https://"
        ):

            url = uri

        else:

            url = (
                self.base_url
                + (
                    uri
                    if uri.startswith("/")
                    else "/" + uri
                )
            )

        can_retry = (
            self._request_can_retry(
                method
            )
        )

        max_attempts = (
            max(
                1,
                int(
                    vars
                    .FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_REQUEST_RETRIES
                ),
            )
            if can_retry
            else 1
        )

        last_error = None

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            if attempt > 1:

                self._new_http_session()

            try:

                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=kwargs.get(
                        "timeout",
                        self._timeout(),
                    ),
                    json=kwargs.get(
                        "json"
                    ),
                )

                if response.status_code in (
                    401,
                    403,
                ):

                    raise IloAuthenticationError(
                        "iLO {} is reachable but authentication failed "
                        "(HTTP {})".format(
                            self.ip,
                            response.status_code,
                        )
                    )

                return response

            except IloAuthenticationError:

                raise

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.SSLError,
            ) as exc:

                last_error = exc

                if (
                    can_retry
                    and attempt < max_attempts
                ):

                    _log(
                        self.host,
                        (
                            "Transient direct-iLO Redfish transport "
                            "error on {} {} (attempt {}/{}): {}. "
                            "Retrying with a fresh connection..."
                        ).format(
                            str(method).upper(),
                            uri,
                            attempt,
                            max_attempts,
                            exc,
                        ),
                    )

                    time.sleep(
                        vars
                        .FOREMAN_PHYSICAL_NETWORK_BOOT_ILO_RETRY_DELAY_SECONDS
                    )

                    continue

                break

        # Critical classification rule:
        # RemoteDisconnected does not mean the iLO is network-unreachable.
        # Test the actual management endpoint before permitting OA fallback.
        if self._tcp_443_reachable():

            raise IloRedfishTransportError(
                (
                    "iLO {} TCP/443 is reachable, but Redfish {} {} "
                    "failed after {} attempt(s): {}. ACTIVE OA fallback "
                    "is suppressed because the iLO itself is reachable."
                ).format(
                    self.ip,
                    str(method).upper(),
                    uri,
                    max_attempts,
                    last_error,
                )
            )

        raise IloUnreachableError(
            (
                "iLO {} is not reachable on TCP/443 after "
                "Redfish retries: {}"
            ).format(
                self.ip,
                last_error,
            )
        )


    def discover_system(self):

        root_response = (
            self.request(
                "GET",
                "/redfish/v1/",
            )
        )

        if root_response.status_code >= 400:

            raise RuntimeError(
                "iLO Redfish root returned HTTP {}: {}".format(
                    root_response.status_code,
                    root_response.text[:500],
                )
            )

        systems_response = (
            self.request(
                "GET",
                "/redfish/v1/Systems/",
            )
        )

        if systems_response.status_code >= 400:

            raise RuntimeError(
                "Unable to read Redfish Systems collection. "
                "HTTP {}: {}".format(
                    systems_response.status_code,
                    systems_response.text[:500],
                )
            )

        members = (
            systems_response.json()
            .get(
                "Members",
                [],
            )
            or []
        )

        for member in members:

            if isinstance(
                member,
                dict,
            ):

                uri = (
                    member.get(
                        "@odata.id"
                    )
                )

                if uri:

                    self.system_uri = (
                        uri
                    )

                    return uri

        # Existing project hardware normally uses /Systems/1/.
        fallback = (
            "/redfish/v1/Systems/1/"
        )

        fallback_response = (
            self.request(
                "GET",
                fallback,
            )
        )

        if fallback_response.status_code == 200:

            self.system_uri = (
                fallback
            )

            return fallback

        raise RuntimeError(
            "No Redfish ComputerSystem resource was found."
        )


    def get_system(self):

        if not self.system_uri:

            self.discover_system()

        response = (
            self.request(
                "GET",
                self.system_uri,
            )
        )

        if response.status_code >= 400:

            raise RuntimeError(
                "Unable to read iLO ComputerSystem. "
                "HTTP {}: {}".format(
                    response.status_code,
                    response.text[:500],
                )
            )

        return response.json()


    @staticmethod
    def get_post_state(
        system_data,
    ):

        oem = (
            system_data.get(
                "Oem",
                {},
            )
            or {}
        )

        hpe = (
            oem.get(
                "Hpe",
                oem.get(
                    "Hp",
                    {},
                ),
            )
            or {}
        )

        return str(
            hpe.get(
                "PostState",
                "Unknown",
            )
            or "Unknown"
        ).strip()


    @staticmethod
    def is_in_post(
        post_state,
    ):

        value = str(
            post_state
            or ""
        ).strip().lower()

        return (
            value.startswith(
                "inpost"
            )
        )


    @staticmethod
    def is_post_lock_response(
        response,
    ):

        try:

            text = (
                response.text
                or ""
            )

        except Exception:

            text = ""

        return (
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_POST_ERROR_STRING
            in text
        )


    def reset(
        self,
        reset_type,
    ):

        system_data = (
            self.get_system()
        )

        actions = (
            system_data.get(
                "Actions",
                {},
            )
            or {}
        )

        reset_action = (
            actions.get(
                "#ComputerSystem.Reset",
                {},
            )
            or {}
        )

        target = (
            reset_action.get(
                "target"
            )
        )

        if not target:

            target = (
                self.system_uri.rstrip("/")
                + "/Actions/ComputerSystem.Reset"
            )

        response = (
            self.request(
                "POST",
                target,
                json={
                    "ResetType":
                        reset_type
                },
            )
        )

        if response.status_code not in (
            200,
            201,
            202,
            204,
        ):

            raise RuntimeError(
                "iLO power command '{}' failed. HTTP {}: {}"
                .format(
                    reset_type,
                    response.status_code,
                    response.text[:500],
                )
            )

        return response


    def wait_for_power_state(
        self,
        desired_state,
    ):

        desired = str(
            desired_state
        ).strip().lower()

        deadline = (
            time.time()
            + vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_POWER_OFF_TIMEOUT_SECONDS
        )

        while time.time() < deadline:

            try:

                current = str(
                    self.get_system()
                    .get(
                        "PowerState",
                        "Unknown",
                    )
                ).strip()

                if current.lower() == desired:

                    return True

            except IloUnreachableError:

                # iLO normally stays reachable while host power changes.
                # If it briefly drops, keep polling.
                pass

            time.sleep(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_POLL_INTERVAL_SECONDS
            )

        return False


    def force_off_for_post(self):

        _log(
            self.host,
            (
                "Server is in POST. Forcing host power OFF "
                "before configuring one-time PXE boot..."
            ),
        )

        self.reset(
            "ForceOff"
        )

        if not self.wait_for_power_state(
            "Off"
        ):

            raise RuntimeError(
                "Server did not reach PowerState=Off "
                "within {} seconds.".format(
                    vars
                    .FOREMAN_PHYSICAL_NETWORK_BOOT_POWER_OFF_TIMEOUT_SECONDS
                )
            )

        _log(
            self.host,
            (
                "Server reached PowerState=Off; "
                "POST lock is cleared."
            ),
        )


    def patch_pxe_once(self):

        payload = {
            "Boot": {
                "BootSourceOverrideTarget":
                    "Pxe",

                "BootSourceOverrideEnabled":
                    "Once",
            }
        }

        response = (
            self.request(
                "PATCH",
                self.system_uri,
                json=payload,
            )
        )

        return response


    def verify_pxe_once(self):

        system_data = (
            self.get_system()
        )

        boot = (
            system_data.get(
                "Boot",
                {},
            )
            or {}
        )

        target = str(
            boot.get(
                "BootSourceOverrideTarget",
                "",
            )
            or ""
        ).strip()

        enabled = str(
            boot.get(
                "BootSourceOverrideEnabled",
                "",
            )
            or ""
        ).strip()

        return (
            target.lower()
            == "pxe"
            and enabled.lower()
            == "once"
        )


    def configure_pxe_once(self):

        system_data = (
            self.get_system()
        )

        power_state = str(
            system_data.get(
                "PowerState",
                "Unknown",
            )
            or "Unknown"
        ).strip()

        post_state = (
            self.get_post_state(
                system_data
            )
        )

        _log(
            self.host,
            (
                "Direct iLO connected. "
                "PowerState={}; PostState={}."
            ).format(
                power_state,
                post_state,
            ),
        )

        powered_off_for_post = False

        # If iLO already reports POST, do not first attempt a write that is
        # expected to be rejected.  Shut down, configure boot while Off, then
        # power the host back on.
        if (
            power_state.lower()
            == "on"
            and self.is_in_post(
                post_state
            )
        ):

            self.force_off_for_post()

            powered_off_for_post = (
                True
            )

        response = (
            self.patch_pxe_once()
        )

        # Defensive race handling: POST can start between GET and PATCH.
        if (
            response.status_code >= 400
            and self.is_post_lock_response(
                response
            )
        ):

            _log(
                self.host,
                (
                    "iLO rejected PXE boot override because "
                    "POST is in progress. Performing POST-safe "
                    "ForceOff -> configure PXE -> power on."
                ),
            )

            if not powered_off_for_post:

                self.force_off_for_post()

                powered_off_for_post = (
                    True
                )

            response = (
                self.patch_pxe_once()
            )

        if response.status_code >= 400:

            raise RuntimeError(
                "Failed to configure one-time PXE boot. "
                "HTTP {}: {}".format(
                    response.status_code,
                    response.text[:700],
                )
            )

        if not self.verify_pxe_once():

            raise RuntimeError(
                "iLO accepted the boot PATCH, but read-back "
                "did not confirm Pxe/Once."
            )

        _log(
            self.host,
            (
                "One-time network/PXE boot verified "
                "through direct iLO Redfish."
            ),
        )

        if powered_off_for_post:

            _log(
                self.host,
                (
                    "Powering host ON after POST-safe "
                    "PXE configuration so network installation "
                    "starts immediately..."
                ),
            )

            self.reset(
                "On"
            )

            return {
                "success":
                    True,

                "status":
                    "Successful",

                "method":
                    "Direct iLO Redfish",

                "details":
                    (
                        "PXE/Once configured; host was in POST, "
                        "was ForceOff, configured while Off, "
                        "and powered On to start PXE installation"
                    ),
            }

        if power_state.lower() == "off":

            _log(
                self.host,
                (
                    "Host is powered OFF. Powering it ON now "
                    "so PXE installation starts immediately..."
                ),
            )

            self.reset(
                "On"
            )

            return {
                "success":
                    True,

                "status":
                    "Successful",

                "method":
                    "Direct iLO Redfish",

                "details":
                    (
                        "PXE/Once configured and verified; "
                        "host was Off and was powered On to "
                        "start PXE installation"
                    ),
            }

        _log(
            self.host,
            (
                "Host is running normally. Rebooting now "
                "so the verified one-time PXE boot is consumed "
                "and installation starts automatically..."
            ),
        )

        self.reset(
            "ForceRestart"
        )

        return {
            "success":
                True,

            "status":
                "Successful",

            "method":
                "Direct iLO Redfish",

            "details":
                (
                    "PXE/Once configured and verified; "
                    "running host was ForceRestarted to "
                    "start PXE installation immediately"
                ),
        }


def _configure_direct_ilo(
    host,
    username,
    password,
    allow_oa_fallback,
):

    client = (
        RedfishBootClient(
            host,
            username,
            password,
        )
    )

    try:

        client.discover_system()

        return (
            client.configure_pxe_once()
        )

    except IloUnreachableError:

        raise

    except Exception as exc:

        return {
            "success":
                False,

            "status":
                "Failed",

            "method":
                "Direct iLO Redfish",

            "details":
                str(
                    exc
                ),
        }

    finally:

        client.close()


# =============================================================================
# BLADE FALLBACK THROUGH ACTIVE OA
# =============================================================================

def _to_slot(value):

    try:

        return int(
            float(
                value
            )
        )

    except Exception:

        return None


def _load_oa_inventory():

    global OA_INVENTORY_CACHE

    with OA_CACHE_LOCK:

        if OA_INVENTORY_CACHE is not None:

            return (
                OA_INVENTORY_CACHE
            )

        workbook = (
            openpyxl.load_workbook(
                vars.RESOURCE_LIST,
                read_only=True,
                data_only=True,
            )
        )

        try:

            worksheet = (
                workbook[
                    vars.SHEET_NAME
                ]
            )

            rows = (
                worksheet.iter_rows(
                    values_only=True
                )
            )

            try:

                header = next(
                    rows
                )

            except StopIteration:

                OA_INVENTORY_CACHE = {}

                return {}

            header_map = {}

            for index, value in enumerate(
                header
            ):

                name = str(
                    value
                    or ""
                ).strip().lower()

                if name:

                    header_map[
                        name
                    ] = index

            required = (
                "enclosure_physical_name",
                "equipment_type",
                "enclosure_slot",
                "ilo_ip",
            )

            missing = [
                name
                for name in required
                if name not in header_map
            ]

            if missing:

                raise RuntimeError(
                    "OA discovery cannot scan workbook; "
                    "missing column(s): {}".format(
                        ", ".join(
                            missing
                        )
                    )
                )

            inventory = {}

            excel_row = 1

            for row in rows:

                excel_row += 1

                enclosure_name = str(
                    row[
                        header_map[
                            "enclosure_physical_name"
                        ]
                    ]
                    or ""
                ).strip()

                equipment_type = str(
                    row[
                        header_map[
                            "equipment_type"
                        ]
                    ]
                    or ""
                ).strip()

                oa_ip = str(
                    row[
                        header_map[
                            "ilo_ip"
                        ]
                    ]
                    or ""
                ).strip()

                slot = (
                    _to_slot(
                        row[
                            header_map[
                                "enclosure_slot"
                            ]
                        ]
                    )
                )

                if (
                    not enclosure_name
                    or equipment_type.lower()
                    != "enclosure oa"
                    or not oa_ip
                ):

                    continue

                key = (
                    enclosure_name.lower()
                )

                inventory.setdefault(
                    key,
                    []
                ).append({
                    "slot":
                        slot,

                    "ip":
                        oa_ip,

                    "excel_row":
                        excel_row,
                })

            for key in inventory:

                inventory[
                    key
                ].sort(
                    key=lambda item: (
                        (
                            item[
                                "slot"
                            ]
                            if item[
                                "slot"
                            ]
                            is not None
                            else 999
                        ),
                        item[
                            "excel_row"
                        ],
                    )
                )

            OA_INVENTORY_CACHE = (
                inventory
            )

            return inventory

        finally:

            workbook.close()


class OAConnection(object):

    def __init__(
        self,
        hostname,
    ):

        self.hostname = hostname
        self.client = None
        self.channel = None


    def connect(self):

        self.close()

        paramiko_module = (
            _load_paramiko()
        )

        self.client = (
            paramiko_module.SSHClient()
        )

        self.client.set_missing_host_key_policy(
            paramiko_module.AutoAddPolicy()
        )

        self.client.connect(
            hostname=self.hostname,
            port=(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_SSH_PORT
            ),
            username=vars.OA_USERNAME,
            password=vars.OA_PASSWORD,
            timeout=(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_CONNECT_TIMEOUT_SECONDS
            ),
            banner_timeout=(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_CONNECT_TIMEOUT_SECONDS
            ),
            auth_timeout=(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_CONNECT_TIMEOUT_SECONDS
            ),
            look_for_keys=False,
            allow_agent=False,
        )

        transport = (
            self.client.get_transport()
        )

        if transport:

            transport.set_keepalive(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_KEEPALIVE_SECONDS
            )

        self.channel = (
            self.client.invoke_shell()
        )

        time.sleep(
            0.5
        )

        self._drain()


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


    def _drain(self):

        output = ""

        if not self.channel:

            return output

        while self.channel.recv_ready():

            data = (
                self.channel.recv(
                    65535
                )
            )

            if not data:

                break

            output += (
                data.decode(
                    "utf-8",
                    errors="replace",
                )
            )

        return output


    def send_command(
        self,
        command,
        timeout=None,
    ):

        if not self.channel:

            raise RuntimeError(
                "OA SSH channel is not connected"
            )

        if timeout is None:

            timeout = (
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_COMMAND_TIMEOUT_SECONDS
            )

        self._drain()

        self.channel.sendall(
            command
            + "\n"
        )

        output = ""
        deadline = (
            time.monotonic()
            + timeout
        )

        quiet_since = None

        while time.monotonic() < deadline:

            if self.channel.recv_ready():

                data = (
                    self.channel.recv(
                        65535
                    )
                )

                if not data:

                    break

                output += (
                    data.decode(
                        "utf-8",
                        errors="replace",
                    )
                )

                quiet_since = None

                if re.search(
                    r"\n[^\n>]*>\s*$",
                    output,
                ):

                    time.sleep(
                        0.1
                    )

                    output += (
                        self._drain()
                    )

                    break

            else:

                if quiet_since is None:

                    quiet_since = (
                        time.monotonic()
                    )

                elif (
                    time.monotonic()
                    - quiet_since
                    >= vars
                    .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_QUIET_SECONDS
                ):

                    break

                time.sleep(
                    0.05
                )

        return output


    def is_active(self):

        output = (
            self.send_command(
                "SHOW OA STATUS"
            )
        )

        return bool(
            re.search(
                r"Role:\s*Active",
                output,
                flags=re.IGNORECASE,
            )
        )


    def execute_hponcfg(
        self,
        bay_number,
        ribcl,
        end_marker,
    ):

        if not self.channel:

            raise RuntimeError(
                "OA SSH channel is not connected"
            )

        self._drain()

        command = (
            "HPONCFG {} << {}\n{}\n{}\n"
            .format(
                bay_number,
                end_marker,
                ribcl.rstrip(),
                end_marker,
            )
        )

        for line in command.splitlines():

            self.channel.sendall(
                line
                + "\n"
            )

            time.sleep(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_LINE_DELAY_SECONDS
            )

        output = ""
        deadline = (
            time.monotonic()
            + vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_COMMAND_TIMEOUT_SECONDS
        )

        quiet_since = None

        while time.monotonic() < deadline:

            if self.channel.recv_ready():

                data = (
                    self.channel.recv(
                        65535
                    )
                )

                if not data:

                    break

                output += (
                    data.decode(
                        "utf-8",
                        errors="replace",
                    )
                )

                quiet_since = None

                if (
                    "END RIBCL RESULTS"
                    in output
                ):

                    time.sleep(
                        0.1
                    )

                    output += (
                        self._drain()
                    )

                    break

            else:

                if quiet_since is None:

                    quiet_since = (
                        time.monotonic()
                    )

                elif (
                    time.monotonic()
                    - quiet_since
                    >= vars
                    .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_QUIET_SECONDS
                ):

                    break

                time.sleep(
                    0.05
                )

        return output


def _find_active_oa(
    host,
):

    enclosure_name = str(
        host.get(
            "enclosure_physical_name",
            "",
        )
        or ""
    ).strip()

    if not enclosure_name:

        raise RuntimeError(
            "Blade host is missing enclosure_physical_name; "
            "ACTIVE OA cannot be discovered."
        )

    inventory = (
        _load_oa_inventory()
    )

    candidates = (
        inventory.get(
            enclosure_name.lower(),
            [],
        )
    )

    if not candidates:

        raise RuntimeError(
            "No Enclosure OA rows were found in the complete "
            "worksheet for enclosure '{}'.".format(
                enclosure_name
            )
        )

    last_error = None

    for candidate in candidates:

        oa_ip = (
            candidate[
                "ip"
            ]
        )

        _log(
            host,
            (
                "Checking OA {} for ACTIVE role..."
            ).format(
                oa_ip
            ),
        )

        oa = (
            OAConnection(
                oa_ip
            )
        )

        try:

            oa.connect()

            if oa.is_active():

                _log(
                    host,
                    (
                        "ACTIVE OA discovered: {}."
                    ).format(
                        oa_ip
                    ),
                )

                return (
                    oa_ip,
                    oa,
                )

            last_error = (
                "OA {} is standby/inactive"
                .format(
                    oa_ip
                )
            )

        except Exception as exc:

            last_error = (
                "OA {} connection/check failed: {}"
                .format(
                    oa_ip,
                    exc,
                )
            )

        oa.close()

    raise RuntimeError(
        last_error
        or "Unable to find ACTIVE OA"
    )


def _build_ribcl_set_network_boot():

    return """<RIBCL VERSION="2.0">
<LOGIN USER_LOGIN={} PASSWORD={}>
<SERVER_INFO MODE="write">
<SET_ONE_TIME_BOOT VALUE="NETWORK"/>
</SERVER_INFO>
</LOGIN>
</RIBCL>""".format(
        quoteattr(
            vars.ILO_BL_USERNAME
        ),
        quoteattr(
            vars.ILO_BL_PASSWORD
        ),
    )


def _build_ribcl_get_network_boot():

    return """<RIBCL VERSION="2.0">
<LOGIN USER_LOGIN={} PASSWORD={}>
<SERVER_INFO MODE="read">
<GET_ONE_TIME_BOOT/>
</SERVER_INFO>
</LOGIN>
</RIBCL>""".format(
        quoteattr(
            vars.ILO_BL_USERNAME
        ),
        quoteattr(
            vars.ILO_BL_PASSWORD
        ),
    )


def _ribcl_statuses(
    output,
):

    return [
        value.upper()
        for value in re.findall(
            r'\bSTATUS\s*=\s*["\']([^"\']+)["\']',
            output,
            flags=re.IGNORECASE,
        )
    ]


def _ribcl_success(
    output,
):

    statuses = (
        _ribcl_statuses(
            output
        )
    )

    return bool(
        statuses
    ) and all(
        status == "0X0000"
        for status in statuses
    )


def _ribcl_post_lock(
    output,
):

    value = str(
        output
        or ""
    ).upper()

    return (
        "0X00D4" in value
        or "POST IN PROGRESS" in value
        or "UNABLETOMODIFYDURINGSYSTEMPOST"
        in value
    )


def _execute_oa_ribcl_with_retry(
    oa,
    slot,
    ribcl,
    marker_prefix,
    host,
):

    attempts = max(
        1,
        int(
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_RIBCL_RETRIES
        ),
    )

    last_output = ""

    for attempt in range(
        1,
        attempts + 1,
    ):

        last_output = oa.execute_hponcfg(
            slot,
            ribcl,
            "{}_{}".format(
                marker_prefix,
                attempt,
            ),
        )

        statuses = (
            _ribcl_statuses(
                last_output
            )
        )

        boot_match = re.search(
            r'<BOOT_TYPE\s+VALUE\s*=\s*["\']([^"\']+)["\']',
            str(
                last_output
                or ""
            ),
            flags=re.IGNORECASE,
        )

        if (
            statuses
            or _ribcl_post_lock(
                last_output
            )
            or boot_match
        ):

            return last_output

        if attempt < attempts:

            _log(
                host,
                (
                    "HPONCFG/RIBCL returned no parseable response "
                    "for bay {} (attempt {}/{}). Retrying..."
                ).format(
                    slot,
                    attempt,
                    attempts,
                ),
            )

            time.sleep(
                vars
                .FOREMAN_PHYSICAL_NETWORK_BOOT_OA_RIBCL_RETRY_DELAY_SECONDS
            )

    return last_output


def _verify_oa_network_boot(
    oa,
    slot,
):

    output = (
        _execute_oa_ribcl_with_retry(
            oa,
            slot,
            _build_ribcl_get_network_boot(),
            "FOREMAN_PXE_VERIFY_EOF",
            {
                "hostname":
                    "blade-bay-{}".format(
                        slot
                    ),

                "_excel_row":
                    "-",

                "ilo_ip":
                    oa.hostname,
            },
        )
    )

    if not _ribcl_success(
        output
    ):

        return False

    return bool(
        re.search(
            r'<BOOT_TYPE\s+VALUE\s*=\s*["\']NETWORK["\']',
            output,
            flags=re.IGNORECASE,
        )
    )


def _oa_power_is_off(
    output,
):

    return bool(
        re.search(
            r"Power:\s*Off\b",
            output,
            flags=re.IGNORECASE,
        )
    )


def _wait_oa_power_off(
    oa,
    slot,
):

    deadline = (
        time.time()
        + vars
        .FOREMAN_PHYSICAL_NETWORK_BOOT_POWER_OFF_TIMEOUT_SECONDS
    )

    while time.time() < deadline:

        output = (
            oa.send_command(
                "SHOW SERVER STATUS {}".format(
                    slot
                )
            )
        )

        if _oa_power_is_off(
            output
        ):

            return True

        time.sleep(
            vars
            .FOREMAN_PHYSICAL_NETWORK_BOOT_POLL_INTERVAL_SECONDS
        )

    return False


def _configure_blade_via_oa(
    host,
):

    slot = (
        _to_slot(
            host.get(
                "enclosure_slot"
            )
        )
    )

    if slot is None:

        return {
            "success":
                False,

            "status":
                "Failed",

            "method":
                "Active OA / HPONCFG",

            "details":
                "Blade enclosure_slot is missing or invalid",
        }

    oa = None
    oa_ip = None

    try:

        (
            oa_ip,
            oa,
        ) = (
            _find_active_oa(
                host
            )
        )

        _log(
            host,
            (
                "Configuring blade bay {} for one-time "
                "NETWORK boot through ACTIVE OA {}..."
            ).format(
                slot,
                oa_ip,
            ),
        )

        set_output = (
            _execute_oa_ribcl_with_retry(
                oa,
                slot,
                _build_ribcl_set_network_boot(),
                "FOREMAN_PXE_SET_EOF",
                host,
            )
        )

        powered_off_for_post = False

        if _ribcl_post_lock(
            set_output
        ):

            _log(
                host,
                (
                    "Blade iLO reports POST in progress through "
                    "HPONCFG. Forcing bay {} OFF before retrying "
                    "one-time network boot..."
                ).format(
                    slot
                ),
            )

            oa.send_command(
                "POWEROFF SERVER {} FORCE".format(
                    slot
                )
            )

            if not (
                _wait_oa_power_off(
                    oa,
                    slot,
                )
            ):

                raise RuntimeError(
                    "Blade bay {} did not reach Power=Off "
                    "within {} seconds.".format(
                        slot,
                        vars
                        .FOREMAN_PHYSICAL_NETWORK_BOOT_POWER_OFF_TIMEOUT_SECONDS,
                    )
                )

            powered_off_for_post = (
                True
            )

            set_output = (
                _execute_oa_ribcl_with_retry(
                    oa,
                    slot,
                    _build_ribcl_set_network_boot(),
                    "FOREMAN_PXE_RETRY_EOF",
                    host,
                )
            )

        if not _ribcl_success(
            set_output
        ):

            statuses = (
                _ribcl_statuses(
                    set_output
                )
            )

            raise RuntimeError(
                "HPONCFG/RIBCL SET_ONE_TIME_BOOT failed. "
                "RIBCL status(es): {}".format(
                    (
                        ", ".join(
                            statuses
                        )
                        if statuses
                        else "No RESPONSE status returned"
                    )
                )
            )

        if not (
            _verify_oa_network_boot(
                oa,
                slot,
            )
        ):

            raise RuntimeError(
                "HPONCFG/RIBCL write completed, but "
                "GET_ONE_TIME_BOOT did not verify NETWORK."
            )

        _log(
            host,
            (
                "One-time NETWORK boot verified through "
                "ACTIVE OA {} for bay {}."
            ).format(
                oa_ip,
                slot,
            ),
        )

        if powered_off_for_post:

            _log(
                host,
                (
                    "Powering blade bay {} ON after "
                    "POST-safe network-boot configuration "
                    "so PXE installation starts immediately..."
                ).format(
                    slot
                ),
            )

            oa.send_command(
                "POWERON SERVER {}".format(
                    slot
                )
            )

            details = (
                "Direct iLO was unreachable; ACTIVE OA {} "
                "used HPONCFG/RIBCL. Blade was in POST, "
                "was forced Off, NETWORK/Once was configured "
                "and verified, then bay {} was powered On "
                "to start PXE installation."
            ).format(
                oa_ip,
                slot,
            )

        else:

            _log(
                host,
                (
                    "Blade bay {} is running normally. "
                    "Rebooting it through ACTIVE OA with PXE "
                    "as the one-time boot device so installation "
                    "starts immediately..."
                ).format(
                    slot
                ),
            )

            reboot_output = (
                oa.send_command(
                    "REBOOT SERVER {} PXE".format(
                        slot
                    )
                )
            )

            reboot_upper = str(
                reboot_output
                or ""
            ).upper()

            if (
                "ERROR" in reboot_upper
                or "INVALID" in reboot_upper
                or "FAILED" in reboot_upper
            ):

                raise RuntimeError(
                    "ACTIVE OA REBOOT SERVER {} PXE command "
                    "reported an error: {}".format(
                        slot,
                        reboot_output.strip()[:700],
                    )
                )

            details = (
                "Direct iLO was unreachable; ACTIVE OA {} "
                "used HPONCFG/RIBCL to configure and verify "
                "NETWORK/Once for bay {}, then REBOOT SERVER "
                "{} PXE was issued to start installation "
                "immediately."
            ).format(
                oa_ip,
                slot,
                slot,
            )

        return {
            "success":
                True,

            "status":
                "Successful",

            "method":
                "Active OA / HPONCFG",

            "details":
                details,
        }

    except Exception as exc:

        return {
            "success":
                False,

            "status":
                "Failed",

            "method":
                (
                    "Active OA / HPONCFG"
                    if oa_ip
                    else "Active OA discovery"
                ),

            "details":
                str(
                    exc
                ),
        }

    finally:

        if oa:

            oa.close()


def _configure_blade(
    host,
):

    ilo_ip = str(
        host.get(
            "ilo_ip",
            "",
        )
        or ""
    ).strip()

    if ilo_ip:

        _log(
            host,
            (
                "Blade server: trying direct iLO {} first..."
            ).format(
                ilo_ip
            ),
        )

        try:

            direct_result = (
                _configure_direct_ilo(
                    host,
                    vars.ILO_BL_USERNAME,
                    vars.ILO_BL_PASSWORD,
                    allow_oa_fallback=True,
                )
            )

            return direct_result

        except IloUnreachableError as exc:

            _log(
                host,
                (
                    "{} TCP/443 reachability check also failed; "
                    "falling back to ACTIVE OA."
                ).format(
                    exc
                ),
            )

    else:

        _log(
            host,
            (
                "Blade iLO IP is missing; trying ACTIVE OA "
                "fallback directly."
            ),
        )

    oa_lock = (
        _get_oa_operation_lock(
            host
        )
    )

    enclosure_name = str(
        host.get(
            "enclosure_physical_name",
            "",
        )
        or "Unknown"
    ).strip()

    _log(
        host,
        (
            "Waiting for serialized ACTIVE OA fallback "
            "slot for enclosure '{}'..."
        ).format(
            enclosure_name
        ),
    )

    with oa_lock:

        _log(
            host,
            (
                "Acquired ACTIVE OA fallback slot for "
                "enclosure '{}'."
            ).format(
                enclosure_name
            ),
        )

        return (
            _configure_blade_via_oa(
                host
            )
        )
