import os
import sys
import time
import re
import urllib3
import requests
import openpyxl
import pandas as pd
import concurrent.futures

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from functions import vars
from functions.output_log import run_logged_main
from functions.reporting import (
    make_summary_row,
    print_summary_report,
    write_summary_csv,
)


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# =============================================================================
# 1. CENTRALIZED CONFIGURATION
# =============================================================================

# Reusable settings are maintained in functions/vars.py. Local names below are
# aliases only; configuration values are not duplicated in this script.

EXCEL_PATH = vars.RESOURCE_LIST
SHEET_NAME = vars.SHEET_NAME
EXCEL_EMPTY_ROW_STOP = vars.RAID_EXCEL_EMPTY_ROW_STOP
START_ROW = vars.START_ROW
END_ROW = vars.END_ROW
LOG_DIR = vars.LOG_DIR

USERNAME = vars.ILO_RM_USERNAME
PASSWORD = vars.ILO_RM_PASSWORD

REQUEST_TIMEOUT_SECONDS = vars.RAID_RM_REQUEST_TIMEOUT_SECONDS
WRITE_TIMEOUT_SECONDS = vars.RAID_RM_WRITE_TIMEOUT_SECONDS

VALID_EQUIPMENT_TYPES = list(vars.RAID_RM_EQUIPMENT_TYPES)
REQUIRED_COLUMNS = list(vars.RAID_RM_REQUIRED_COLUMNS)

RAID_LEVEL = vars.RAID_LEVEL
RAID_DISPLAY_NAME = vars.RAID_DISPLAY_NAME
RAID_DATA_DRIVE_COUNT = vars.RAID_DATA_DRIVE_COUNT
RAID_CAPACITY_GIB = vars.RAID_CAPACITY_GIB

MAX_WORKERS = vars.RAID_MAX_WORKERS

CONTROLLER_TIMEOUT_MINUTES = vars.RAID_CONTROLLER_TIMEOUT_MINUTES
RAID_TIMEOUT_MINUTES = vars.RAID_TIMEOUT_MINUTES
POLL_INTERVAL_SECONDS = vars.RAID_POLL_INTERVAL_SECONDS

AUTH_RETRIES = vars.RAID_AUTH_RETRIES
AUTH_RETRY_DELAY_SECONDS = vars.RAID_AUTH_RETRY_DELAY_SECONDS
HTTP_RETRY_TOTAL = vars.RAID_HTTP_RETRY_TOTAL
HTTP_RETRY_BACKOFF_FACTOR = vars.RAID_HTTP_RETRY_BACKOFF_FACTOR
HTTP_RETRY_STATUS_CODES = vars.RAID_HTTP_RETRY_STATUS_CODES

REBOOT_DETECTION_TIMEOUT_SECONDS = (
    vars.RAID_RM_REBOOT_DETECTION_TIMEOUT_SECONDS
)
REBOOT_DETECTION_POLL_SECONDS = (
    vars.RAID_RM_REBOOT_DETECTION_POLL_SECONDS
)
POWER_OFF_TIMEOUT_SECONDS = vars.RAID_RM_POWER_OFF_TIMEOUT_SECONDS
POWER_ON_INITIAL_WAIT_SECONDS = (
    vars.RAID_RM_POWER_ON_INITIAL_WAIT_SECONDS
)

REPORT_PREFIX = vars.RAID_RM_REPORT_PREFIX


# =============================================================================
# 2. HELPERS
# =============================================================================

def log(row_number, ip, message):

    row_str = (
        f"{int(row_number):04}"
        if isinstance(row_number, (int, float))
        else "????"
    )

    print(
        f"[Row {row_str} | {ip}] {message}",
        flush=True,
    )


def natural_sort_key(value):

    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(
            r"(\d+)",
            str(value),
        )
    ]


def get_member_uri(member):

    if not isinstance(member, dict):
        return None

    return (
        member.get("@odata.id")
        or member.get("href")
    )


def get_link_uri(data, key):

    if not isinstance(data, dict):
        return None

    # Standard Links
    for links_key in (
        "Links",
        "links",
    ):

        links = data.get(
            links_key,
            {},
        )

        if not isinstance(links, dict):
            continue

        value = links.get(key)

        if isinstance(value, dict):

            return (
                value.get("@odata.id")
                or value.get("href")
            )

        if isinstance(value, str):
            return value

    # Direct property
    value = data.get(key)

    if isinstance(value, dict):

        return (
            value.get("@odata.id")
            or value.get("href")
        )

    if isinstance(value, str):
        return value

    return None


# =============================================================================
# 3. EXCEL LOADER
# =============================================================================

def load_resource_excel_fast(
    filepath,
    sheet_name,
    start_row=2,
    end_row=None,
    empty_row_stop=25,
):

    if start_row is None:
        start_row = 2

    start_row = int(start_row)

    if start_row < 2:

        raise ValueError(
            "START_ROW must be >= 2."
        )

    if end_row is not None:

        end_row = int(end_row)

        if end_row < start_row:

            raise ValueError(
                "END_ROW must be >= START_ROW."
            )

    wb = openpyxl.load_workbook(
        filepath,
        read_only=True,
        data_only=True,
    )

    try:

        if sheet_name not in wb.sheetnames:

            raise ValueError(
                f"Sheet '{sheet_name}' not found."
            )

        ws = wb[sheet_name]

        header_values = next(
            ws.iter_rows(
                min_row=1,
                max_row=1,
                values_only=True,
            ),
            None,
        )

        if not header_values:
            return pd.DataFrame()

        headers = [

            (
                str(cell).strip()
                if cell is not None
                and str(cell).strip() != ""
                else f"Unnamed_{index}"
            )

            for index, cell
            in enumerate(header_values)
        ]

        data = []
        excel_rows = []

        empty_count = 0

        for excel_row, row in enumerate(
            ws.iter_rows(
                min_row=2,
                values_only=True,
            ),
            start=2,
        ):

            if excel_row < start_row:
                continue

            if (
                end_row is not None
                and excel_row > end_row
            ):
                break

            is_empty = all(
                cell is None
                or str(cell).strip() == ""
                for cell in row
            )

            if is_empty:

                empty_count += 1

                if empty_count >= empty_row_stop:
                    break

                continue

            empty_count = 0

            normalized = tuple(
                row[:len(headers)]
            )

            if len(normalized) < len(headers):

                normalized += (
                    None,
                ) * (
                    len(headers)
                    - len(normalized)
                )

            data.append(normalized)
            excel_rows.append(excel_row)

        df = pd.DataFrame(
            data,
            columns=headers,
        )

        if not df.empty:

            df.insert(
                0,
                "_excel_row",
                excel_rows,
            )

        return df

    finally:

        wb.close()


# =============================================================================
# 4. SERVER PROCESSOR
# =============================================================================

class ServerProcessor:

    def __init__(
        self,
        ip,
        row_number,
        username,
        password,
    ):

        self.ip = ip
        self.row_number = row_number

        self.base_url = (
            f"https://{ip}"
        )

        self.username = username
        self.password = password

        self.system_uri = None

        self.session = requests.Session()

        self.session.verify = False

        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "OData-Version": "4.0",
            }
        )

        retries = Retry(
            total=HTTP_RETRY_TOTAL,
            connect=HTTP_RETRY_TOTAL,
            read=HTTP_RETRY_TOTAL,
            status=HTTP_RETRY_TOTAL,
            backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
            status_forcelist=list(
                HTTP_RETRY_STATUS_CODES
            ),
            allowed_methods=frozenset(
                [
                    "GET",
                    "HEAD",
                    "OPTIONS",
                ]
            ),
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retries,
        )

        self.session.mount(
            "https://",
            adapter,
        )


    # =========================================================================
    # HTTP
    # =========================================================================

    def _request(
        self,
        method,
        uri,
        **kwargs,
    ):

        kwargs.setdefault(
            "timeout",
            REQUEST_TIMEOUT_SECONDS,
        )

        if uri.startswith("http"):

            url = uri

        else:

            url = (
                f"{self.base_url}"
                f"{uri}"
            )

        return self.session.request(
            method,
            url,
            **kwargs,
        )


    def _get_json(
        self,
        uri,
    ):

        response = self._request(
            "GET",
            uri,
        )

        response.raise_for_status()

        return response.json()


    # =========================================================================
    # AUTH
    # =========================================================================

    def authenticate(
        self,
        retries=AUTH_RETRIES,
    ):

        for attempt in range(
            1,
            retries + 1,
        ):

            try:

                response = self._request(
                    "POST",
                    (
                        "/redfish/v1/"
                        "SessionService/"
                        "Sessions/"
                    ),
                    json={
                        "UserName":
                            self.username,
                        "Password":
                            self.password,
                    },
                )

                response.raise_for_status()

                token = (
                    response.headers.get(
                        "X-Auth-Token"
                    )
                )

                if not token:

                    raise Exception(
                        "iLO did not return X-Auth-Token."
                    )

                self.session.headers.update(
                    {
                        "X-Auth-Token":
                            token
                    }
                )

                self.discover_system()

                return

            except Exception as exc:

                if attempt >= retries:

                    raise Exception(
                        "Authentication failed "
                        f"after {retries} attempts: "
                        f"{exc}"
                    )

                log(
                    self.row_number,
                    self.ip,
                    (
                        "Authentication failed/busy. "
                        f"Retrying in {AUTH_RETRY_DELAY_SECONDS} seconds... "
                        f"(Attempt "
                        f"{attempt + 1}/{retries})"
                    ),
                )

                time.sleep(AUTH_RETRY_DELAY_SECONDS)


    # =========================================================================
    # SYSTEM DISCOVERY
    # =========================================================================

    def discover_system(self):

        root = self._get_json(
            "/redfish/v1/"
        )

        systems_uri = (
            root.get(
                "Systems",
                {},
            )
            .get(
                "@odata.id"
            )
        )

        if not systems_uri:

            raise Exception(
                "Systems resource not found."
            )

        systems = self._get_json(
            systems_uri
        )

        members = systems.get(
            "Members",
            [],
        )

        if not members:

            raise Exception(
                "No ComputerSystem found."
            )

        self.system_uri = (
            get_member_uri(
                members[0]
            )
        )

        if not self.system_uri:

            raise Exception(
                "Unable to determine ComputerSystem URI."
            )


    def get_system_info(self):

        if not self.system_uri:
            self.discover_system()

        data = self._get_json(
            self.system_uri
        )

        oem = (
            data.get(
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

        return {
            "PowerState":
                data.get(
                    "PowerState",
                    "Unknown",
                ),

            "PostState":
                hpe.get(
                    "PostState",
                    "Unknown",
                ),

            "Data":
                data,
        }


    # =========================================================================
    # SMART STORAGE INVENTORY
    #
    # IMPORTANT:
    #
    # This is the READ/INVENTORY interface.
    #
    # Existing RAID volumes are discovered here even when
    # SmartStorageConfig is unavailable.
    # =========================================================================

    def get_smartstorage_inventory(self):

        if not self.system_uri:
            self.discover_system()

        collection_uri = (
            self.system_uri.rstrip("/")
            + "/SmartStorage/ArrayControllers/"
        )

        try:

            response = self._request(
                "GET",
                collection_uri,
            )

            if response.status_code == 404:

                return []

            response.raise_for_status()

            members = (
                response.json()
                .get(
                    "Members",
                    [],
                )
            )

        except Exception:

            return []

        controllers = []

        for member in members:

            controller_uri = (
                get_member_uri(
                    member
                )
            )

            if not controller_uri:
                continue

            try:

                controller_data = (
                    self._get_json(
                        controller_uri
                    )
                )

            except Exception:

                continue

            logical_drives = []
            physical_drives = []

            # -----------------------------------------------------------------
            # Logical Drives
            # -----------------------------------------------------------------

            logical_uri = (
                get_link_uri(
                    controller_data,
                    "LogicalDrives",
                )
            )

            if not logical_uri:

                logical_uri = (
                    controller_uri.rstrip("/")
                    + "/LogicalDrives/"
                )

            try:

                logical_collection = (
                    self._get_json(
                        logical_uri
                    )
                )

                for ld_member in (
                    logical_collection.get(
                        "Members",
                        [],
                    )
                ):

                    ld_uri = (
                        get_member_uri(
                            ld_member
                        )
                    )

                    if not ld_uri:
                        continue

                    try:

                        ld_data = (
                            self._get_json(
                                ld_uri
                            )
                        )

                        ld_data[
                            "_uri"
                        ] = ld_uri

                        logical_drives.append(
                            ld_data
                        )

                    except Exception:

                        pass

            except Exception:

                pass

            # -----------------------------------------------------------------
            # Physical Drives
            # -----------------------------------------------------------------

            drive_uri = (
                get_link_uri(
                    controller_data,
                    "DiskDrives",
                )
            )

            if not drive_uri:

                drive_uri = (
                    controller_uri.rstrip("/")
                    + "/DiskDrives/"
                )

            try:

                drive_collection = (
                    self._get_json(
                        drive_uri
                    )
                )

                for drive_member in (
                    drive_collection.get(
                        "Members",
                        [],
                    )
                ):

                    member_uri = (
                        get_member_uri(
                            drive_member
                        )
                    )

                    if not member_uri:
                        continue

                    try:

                        drive_data = (
                            self._get_json(
                                member_uri
                            )
                        )

                        drive_data[
                            "_uri"
                        ] = member_uri

                        physical_drives.append(
                            drive_data
                        )

                    except Exception:

                        pass

            except Exception:

                pass

            controllers.append(
                {
                    "uri":
                        controller_uri,

                    "data":
                        controller_data,

                    "logical_drives":
                        logical_drives,

                    "physical_drives":
                        physical_drives,
                }
            )

        return controllers


    # =========================================================================
    # DMTF STORAGE FALLBACK
    #
    # Used primarily for detecting an existing volume if SmartStorage is
    # unavailable on a newer iLO 5 firmware.
    # =========================================================================

    def get_dmtf_existing_volumes(self):

        if not self.system_uri:
            self.discover_system()

        storage_uri = (
            self.system_uri.rstrip("/")
            + "/Storage/"
        )

        try:

            response = self._request(
                "GET",
                storage_uri,
            )

            if response.status_code == 404:
                return []

            response.raise_for_status()

            storage_members = (
                response.json()
                .get(
                    "Members",
                    [],
                )
            )

        except Exception:

            return []

        volumes = []

        for member in storage_members:

            member_uri = (
                get_member_uri(
                    member
                )
            )

            if not member_uri:
                continue

            try:

                storage_data = (
                    self._get_json(
                        member_uri
                    )
                )

            except Exception:

                continue

            volumes_uri = (
                get_link_uri(
                    storage_data,
                    "Volumes",
                )
            )

            if not volumes_uri:

                volumes_uri = (
                    member_uri.rstrip("/")
                    + "/Volumes/"
                )

            try:

                volume_collection = (
                    self._get_json(
                        volumes_uri
                    )
                )

            except Exception:

                continue

            for volume_member in (
                volume_collection.get(
                    "Members",
                    [],
                )
            ):

                volume_uri = (
                    get_member_uri(
                        volume_member
                    )
                )

                if not volume_uri:
                    continue

                try:

                    volume_data = (
                        self._get_json(
                            volume_uri
                        )
                    )

                    volume_data[
                        "_uri"
                    ] = volume_uri

                    volumes.append(
                        volume_data
                    )

                except Exception:

                    pass

        return volumes


    # =========================================================================
    # EXISTING RAID DETECTION
    # =========================================================================

    def get_existing_logical_drives(self):

        controllers = (
            self.get_smartstorage_inventory()
        )

        logical_drives = []

        for controller in controllers:

            logical_drives.extend(
                controller[
                    "logical_drives"
                ]
            )

        if logical_drives:

            return (
                logical_drives,
                "SmartStorage",
                controllers,
            )

        # ---------------------------------------------------------------------
        # DMTF fallback
        # ---------------------------------------------------------------------

        dmtf_volumes = (
            self.get_dmtf_existing_volumes()
        )

        if dmtf_volumes:

            return (
                dmtf_volumes,
                "DMTF Storage",
                controllers,
            )

        return (
            [],
            "None",
            controllers,
        )


    # =========================================================================
    # SMART STORAGE CONFIG DISCOVERY
    #
    # This is the WRITE/STAGING interface.
    # =========================================================================

    def _collect_config_links(
        self,
        obj,
        found=None,
    ):

        if found is None:
            found = set()

        if isinstance(
            obj,
            dict,
        ):

            uri = (
                obj.get(
                    "@odata.id"
                )
            )

            if isinstance(
                uri,
                str,
            ):

                normalized = (
                    uri.rstrip("/")
                )

                if (
                    "smartstorageconfig"
                    in normalized.lower()
                    and not normalized
                    .lower()
                    .endswith(
                        "/settings"
                    )
                ):

                    found.add(
                        normalized
                    )

            for value in obj.values():

                self._collect_config_links(
                    value,
                    found,
                )

        elif isinstance(
            obj,
            list,
        ):

            for value in obj:

                self._collect_config_links(
                    value,
                    found,
                )

        return found


    def discover_smartstorage_configs(self):

        if not self.system_uri:
            self.discover_system()

        candidates = set()

        # Discover advertised links from ComputerSystem.
        try:

            system_data = (
                self._get_json(
                    self.system_uri
                )
            )

            candidates.update(
                self._collect_config_links(
                    system_data
                )
            )

        except Exception:

            pass

        # Known iLO 5 URI forms.
        candidates.add(
            self.system_uri.rstrip("/")
            + "/SmartStorageConfig"
        )

        for index in range(
            2,
            17,
        ):

            candidates.add(
                self.system_uri.rstrip("/")
                + f"/SmartStorageConfig{index}"
            )

        discovered = []

        for uri in sorted(
            candidates,
            key=natural_sort_key,
        ):

            try:

                response = self._request(
                    "GET",
                    uri + "/",
                )

                if response.status_code in (
                    404,
                    405,
                ):
                    continue

                response.raise_for_status()

                data = response.json()

                canonical_uri = (
                    str(
                        data.get(
                            "@odata.id",
                            uri,
                        )
                    )
                    .rstrip("/")
                )

                discovered.append(
                    {
                        "uri":
                            canonical_uri,

                        "data":
                            data,
                    }
                )

            except Exception:

                continue

        # Deduplicate
        unique = {}

        for config in discovered:

            unique[
                config["uri"]
            ] = config

        return list(
            unique.values()
        )


    # =========================================================================
    # CONFIG DRIVE LOCATIONS
    # =========================================================================

    def get_config_drive_locations(
        self,
        config_data,
    ):

        locations = []

        for drive in (
            config_data.get(
                "PhysicalDrives",
                [],
            )
            or []
        ):

            if not isinstance(
                drive,
                dict,
            ):
                continue

            location = (
                drive.get(
                    "Location"
                )
            )

            if location:

                locations.append(
                    str(location)
                )

        return sorted(
            locations,
            key=natural_sort_key,
        )


    # =========================================================================
    # SELECT SMARTSTORAGECONFIG
    # =========================================================================

    def select_smartstorage_config(self):

        configs = (
            self.discover_smartstorage_configs()
        )

        if not configs:

            return (
                None,
                [],
                None,
            )

        ranked = []

        for config in configs:

            locations = (
                self.get_config_drive_locations(
                    config["data"]
                )
            )

            # Prefer configs containing enough physical disks.
            score = (
                1
                if len(locations)
                >= RAID_DATA_DRIVE_COUNT
                else 0,

                len(locations),
            )

            ranked.append(
                (
                    score,
                    config,
                    locations,
                )
            )

        ranked.sort(
            key=lambda item:
                item[0],
            reverse=True,
        )

        (
            _,
            selected,
            locations,
        ) = ranked[0]

        return (
            selected[
                "uri"
            ],
            locations,
            selected[
                "data"
            ],
        )


    # =========================================================================
    # BOOT TARGET
    # =========================================================================

    def set_boot_to_system_utilities(self):

        info = (
            self.get_system_info()
        )

        system_data = (
            info[
                "Data"
            ]
        )

        boot = (
            system_data.get(
                "Boot",
                {},
            )
            or {}
        )

        allowable = (
            boot.get(
                "BootSourceOverrideTarget@Redfish.AllowableValues",
                [],
            )
            or []
        )

        # HPE System Utilities is normally reached through BiosSetup.
        # If this firmware only advertises Utilities, use that.
        if (
            not allowable
            or "BiosSetup" in allowable
        ):

            target = "BiosSetup"

        elif "Utilities" in allowable:

            target = "Utilities"

        else:

            raise Exception(
                "iLO does not advertise BiosSetup or "
                f"Utilities boot target. "
                f"Allowable targets: {allowable}"
            )

        payload = {
            "Boot": {
                "BootSourceOverrideTarget":
                    target,

                "BootSourceOverrideEnabled":
                    "Once",
            }
        }

        log(
            self.row_number,
            self.ip,
            (
                "Setting one-time boot target "
                f"to System Utilities ({target})..."
            ),
        )

        response = self._request(
            "PATCH",
            self.system_uri,
            json=payload,
        )

        if response.status_code >= 400:

            raise Exception(
                "Failed to set System Utilities "
                f"boot override: HTTP "
                f"{response.status_code}: "
                f"{response.text[:500]}"
            )

        return target


    def set_boot_to_normal(self):

        try:

            response = self._request(
                "PATCH",
                self.system_uri,
                json={
                    "Boot": {
                        "BootSourceOverrideEnabled":
                            "Disabled",
                    }
                },
            )

            # Compatibility fallback
            if response.status_code >= 400:

                self._request(
                    "PATCH",
                    self.system_uri,
                    json={
                        "Boot": {
                            "BootSourceOverrideTarget":
                                "None"
                        }
                    },
                )

        except Exception:

            pass


    # =========================================================================
    # RESET ACTION DISCOVERY
    # =========================================================================

    def get_reset_action(self):

        info = (
            self.get_system_info()
        )

        data = (
            info[
                "Data"
            ]
        )

        actions = (
            data.get(
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
            or reset_action.get(
                "Target"
            )
        )

        if not target:

            target = (
                self.system_uri.rstrip("/")
                + "/Actions/ComputerSystem.Reset"
            )

        allowable = (
            reset_action.get(
                "ResetType@Redfish.AllowableValues",
                [],
            )
            or []
        )

        return (
            target,
            allowable,
        )


    def reset_server(
        self,
        reset_type,
    ):

        target, allowable = (
            self.get_reset_action()
        )

        if (
            allowable
            and reset_type not in allowable
        ):

            raise Exception(
                f"ResetType '{reset_type}' "
                "not supported. "
                f"Allowable={allowable}"
            )

        response = self._request(
            "POST",
            target,
            json={
                "ResetType":
                    reset_type
            },
            timeout=WRITE_TIMEOUT_SECONDS,
        )

        if response.status_code >= 400:

            raise Exception(
                f"{reset_type} failed: "
                f"HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )


    # =========================================================================
    # VERIFY REBOOT
    # =========================================================================

    def wait_for_post_transition(
        self,
        initial_post_state,
        timeout_seconds,
    ):

        deadline = (
            time.time()
            + timeout_seconds
        )

        while time.time() < deadline:

            time.sleep(
                REBOOT_DETECTION_POLL_SECONDS
            )

            try:

                info = (
                    self.get_system_info()
                )

                post_state = str(
                    info.get(
                        "PostState",
                        "Unknown",
                    )
                )

                power_state = str(
                    info.get(
                        "PowerState",
                        "Unknown",
                    )
                )

                if (
                    power_state.lower()
                    != "on"
                ):

                    return True

                if (
                    post_state
                    not in (
                        initial_post_state,
                        "Unknown",
                        "",
                    )
                ):

                    log(
                        self.row_number,
                        self.ip,
                        (
                            "Reboot/POST transition detected: "
                            f"{initial_post_state} -> "
                            f"{post_state}"
                        ),
                    )

                    return True

                if post_state not in (
                    "FinishedPost",
                    "Unknown",
                    "",
                ):

                    return True

            except Exception:

                # Temporary Redfish interruption itself is evidence
                # that iLO/host is transitioning.
                continue

        return False


    # =========================================================================
    # FORCE POWER CYCLE
    # =========================================================================

    def force_power_cycle(self):

        log(
            self.row_number,
            self.ip,
            (
                "ForceRestart did not produce a "
                "detectable POST transition. "
                "Falling back to ForceOff -> On..."
            ),
        )

        try:

            self.reset_server(
                "ForceOff"
            )

        except Exception as exc:

            raise Exception(
                "ForceRestart did not initiate POST "
                "and ForceOff fallback failed: "
                f"{exc}"
            )

        deadline = (
            time.time()
            + POWER_OFF_TIMEOUT_SECONDS
        )

        powered_off = False

        while time.time() < deadline:

            time.sleep(5)

            try:

                state = (
                    self.get_system_info()
                    .get(
                        "PowerState",
                        "Unknown",
                    )
                )

                if (
                    str(state).lower()
                    == "off"
                ):

                    powered_off = True
                    break

            except Exception:

                pass

        if not powered_off:

            raise Exception(
                "Server did not reach PowerState=Off "
                f"within {POWER_OFF_TIMEOUT_SECONDS}s."
            )

        log(
            self.row_number,
            self.ip,
            "Server is powered off. Powering on...",
        )

        self.reset_server(
            "On"
        )

        time.sleep(
            POWER_ON_INITIAL_WAIT_SECONDS
        )


    # =========================================================================
    # REBOOT INTO SYSTEM UTILITIES
    # =========================================================================

    def reboot_to_system_utilities(self):

        boot_target = (
            self.set_boot_to_system_utilities()
        )

        info = (
            self.get_system_info()
        )

        power_state = str(
            info.get(
                "PowerState",
                "Unknown",
            )
        )

        initial_post_state = str(
            info.get(
                "PostState",
                "Unknown",
            )
        )

        if (
            power_state.lower()
            == "off"
        ):

            log(
                self.row_number,
                self.ip,
                (
                    "Server is powered off. "
                    "Powering on into System Utilities..."
                ),
            )

            self.reset_server(
                "On"
            )

            return boot_target

        log(
            self.row_number,
            self.ip,
            (
                "Rebooting server into "
                "System Utilities..."
            ),
        )

        try:

            self.reset_server(
                "ForceRestart"
            )

        except Exception as exc:

            log(
                self.row_number,
                self.ip,
                (
                    "ForceRestart request failed: "
                    f"{exc}"
                ),
            )

            self.force_power_cycle()

            return boot_target

        # ---------------------------------------------------------------------
        # Confirm that ForceRestart actually caused a reboot.
        # ---------------------------------------------------------------------

        reboot_detected = (
            self.wait_for_post_transition(
                initial_post_state,
                REBOOT_DETECTION_TIMEOUT_SECONDS,
            )
        )

        if not reboot_detected:

            self.force_power_cycle()

        return boot_target


    # =========================================================================
    # NORMAL REBOOT
    # =========================================================================

    def reboot_normal(self):

        self.set_boot_to_normal()

        info = (
            self.get_system_info()
        )

        if (
            str(
                info.get(
                    "PowerState",
                    "Unknown",
                )
            ).lower()
            == "off"
        ):

            self.reset_server(
                "On"
            )

            return

        try:

            self.reset_server(
                "ForceRestart"
            )

        except Exception:

            self.force_power_cycle()


    # =========================================================================
    # WAIT FOR STORAGE
    # =========================================================================

    def wait_for_storage(
        self,
        timeout_minutes,
        require_config=False,
    ):

        max_attempts = max(
            1,
            int(
                (
                    timeout_minutes
                    * 60
                )
                / POLL_INTERVAL_SECONDS
            ),
        )

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            controllers = (
                self.get_smartstorage_inventory()
            )

            config_uri = None
            drive_locations = []
            config_data = None

            if require_config:

                (
                    config_uri,
                    drive_locations,
                    config_data,
                ) = (
                    self.select_smartstorage_config()
                )

            inventory_ok = bool(
                controllers
            )

            config_ok = (
                bool(config_uri)
                if require_config
                else True
            )

            if (
                inventory_ok
                and config_ok
            ):

                return (
                    controllers,
                    config_uri,
                    drive_locations,
                    config_data,
                )

            if (
                attempt == 1
                or attempt % 2 == 1
            ):

                log(
                    self.row_number,
                    self.ip,
                    (
                        "Waiting for Smart Array "
                        "inventory/configuration... "
                        f"(Attempt "
                        f"{attempt}/{max_attempts})"
                    ),
                )

            time.sleep(
                POLL_INTERVAL_SECONDS
            )

        return (
            [],
            None,
            [],
            None,
        )


    # =========================================================================
    # STAGE RAID1
    # =========================================================================

    def stage_raid1_configuration(
        self,
        config_uri,
        drive_locations,
    ):

        if (
            len(drive_locations)
            < RAID_DATA_DRIVE_COUNT
        ):

            raise Exception(
                f"Only {len(drive_locations)} "
                "physical drive(s) are visible "
                "through SmartStorageConfig; "
                f"RAID1 requires "
                f"{RAID_DATA_DRIVE_COUNT}."
            )

        selected_drives = sorted(
            drive_locations,
            key=natural_sort_key,
        )[
            :RAID_DATA_DRIVE_COUNT
        ]

        settings_uri = (
            config_uri.rstrip("/")
            + "/Settings/"
        )

        payload = {

            "DataGuard":
                "Disabled",

            "LogicalDrives": [
                {
                    "LogicalDriveName":
                        RAID_DISPLAY_NAME,

                    "Raid":
                        RAID_LEVEL,

                    "CapacityGiB":
                        RAID_CAPACITY_GIB,

                    "DataDrives":
                        selected_drives,

                    "LegacyBootPriority":
                        "Primary",
                }
            ],
        }

        log(
            self.row_number,
            self.ip,
            (
                f"Staging {RAID_LEVEL} "
                "using physical drives: "
                f"{', '.join(selected_drives)}"
            ),
        )

        response = self._request(
            "PUT",
            settings_uri,
            json=payload,
            timeout=WRITE_TIMEOUT_SECONDS,
        )

        if response.status_code >= 400:

            raise Exception(
                "Failed to stage RAID configuration. "
                f"HTTP {response.status_code}: "
                f"{response.text[:1000]}"
            )

        return selected_drives


    # =========================================================================
    # RAID VERIFICATION
    # =========================================================================

    def poll_for_raid(
        self,
        baseline_count,
        timeout_minutes,
    ):

        max_attempts = max(
            1,
            int(
                (
                    timeout_minutes
                    * 60
                )
                / POLL_INTERVAL_SECONDS
            ),
        )

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            time.sleep(
                POLL_INTERVAL_SECONDS
            )

            try:

                (
                    logical_drives,
                    source,
                    controllers,
                ) = (
                    self.get_existing_logical_drives()
                )

                current_count = len(
                    logical_drives
                )

                if (
                    current_count > 0
                    and (
                        baseline_count == 0
                        or current_count
                        != baseline_count
                    )
                ):

                    log(
                        self.row_number,
                        self.ip,
                        (
                            "SUCCESS: RAID logical volume "
                            f"detected through {source}. "
                            f"Logical drives={current_count}"
                        ),
                    )

                    return True

                # With overwrite, number of logical drives can remain the same.
                if (
                    current_count > 0
                    and baseline_count > 0
                ):

                    for logical_drive in logical_drives:

                        raid_value = str(
                            logical_drive.get(
                                "Raid",
                                logical_drive.get(
                                    "RAIDType",
                                    logical_drive.get(
                                        "VolumeType",
                                        "",
                                    ),
                                ),
                            )
                        ).lower()

                        if (
                            "raid1" in raid_value
                            or "mirrored" in raid_value
                        ):

                            log(
                                self.row_number,
                                self.ip,
                                (
                                    "SUCCESS: RAID1 logical "
                                    f"volume detected via {source}."
                                ),
                            )

                            return True

            except Exception:

                pass

            if (
                attempt == 1
                or attempt % 2 == 1
            ):

                log(
                    self.row_number,
                    self.ip,
                    (
                        "Polling RAID inventory... "
                        f"(Attempt "
                        f"{attempt}/{max_attempts})"
                    ),
                )

        return False


# =============================================================================
# 5. SERVER WORKER
# =============================================================================

def process_server(
    server_data,
    overwrite_raid,
    ctrl_timeout,
    raid_timeout,
):

    ip = (
        server_data[
            "ilo_ip"
        ]
    )

    row_number = (
        server_data[
            "excel_row"
        ]
    )

    server = ServerProcessor(
        ip,
        row_number,
        USERNAME,
        PASSWORD,
    )

    booted_to_utilities = False

    try:

        log(
            row_number,
            ip,
            (
                "Starting DL380 Gen10+ "
                "RAID configuration process..."
            ),
        )

        server.authenticate()

        # =====================================================================
        # FIRST: READ EXISTING RAID WHILE CURRENT OS IS RUNNING
        #
        # Do NOT require SmartStorageConfig just to inspect existing RAID.
        # =====================================================================

        log(
            row_number,
            ip,
            (
                "Reading existing Smart Array "
                "inventory while server is online..."
            ),
        )

        (
            existing_ld,
            inventory_source,
            controllers,
        ) = (
            server.get_existing_logical_drives()
        )

        if existing_ld:

            log(
                row_number,
                ip,
                (
                    f"Existing RAID detected via "
                    f"{inventory_source}: "
                    f"{len(existing_ld)} logical "
                    "volume(s)."
                ),
            )

            if not overwrite_raid:

                log(
                    row_number,
                    ip,
                    (
                        "Existing RAID found. "
                        "Skipping because Overwrite=No."
                    ),
                )

                return {
                    "row":
                        row_number,

                    "ip":
                        ip,

                    "status":
                        "Skipped",

                    "time_seconds":
                        0.0,

                    "reason":
                        (
                            "Existing RAID found "
                            f"via {inventory_source} "
                            f"({len(existing_ld)} volume(s))"
                        ),
                }

            log(
                row_number,
                ip,
                (
                    "Overwrite enabled; existing "
                    "RAID will be replaced."
                ),
            )

        else:

            log(
                row_number,
                ip,
                (
                    "No existing logical drive "
                    "detected from online inventory."
                ),
            )

        baseline_count = len(
            existing_ld
        )

        # =====================================================================
        # DISCOVER WRITE CONFIGURATION
        # =====================================================================

        (
            config_uri,
            drive_locations,
            config_data,
        ) = (
            server.select_smartstorage_config()
        )

        # =====================================================================
        # FALLBACK:
        #
        # If either controller inventory or SmartStorageConfig is unavailable,
        # explicitly boot to HPE System Utilities.
        # =====================================================================

        if (
            not controllers
            or not config_uri
        ):

            if not controllers:

                reason = (
                    "Smart Array inventory not visible"
                )

            else:

                reason = (
                    "SmartStorageConfig write interface "
                    "not visible"
                )

            log(
                row_number,
                ip,
                (
                    f"{reason}. "
                    "Rebooting to System Utilities "
                    "to initialize/expose storage..."
                ),
            )

            server.reboot_to_system_utilities()

            booted_to_utilities = True

            (
                controllers,
                config_uri,
                drive_locations,
                config_data,
            ) = (
                server.wait_for_storage(
                    ctrl_timeout,
                    require_config=True,
                )
            )

            # -----------------------------------------------------------------
            # Once in utilities, check existing RAID AGAIN.
            # -----------------------------------------------------------------

            (
                existing_ld_after_boot,
                inventory_source_after_boot,
                _,
            ) = (
                server.get_existing_logical_drives()
            )

            if existing_ld_after_boot:

                log(
                    row_number,
                    ip,
                    (
                        "Existing RAID became visible "
                        "after entering System Utilities: "
                        f"{len(existing_ld_after_boot)} "
                        "logical volume(s)."
                    ),
                )

                baseline_count = len(
                    existing_ld_after_boot
                )

                if not overwrite_raid:

                    log(
                        row_number,
                        ip,
                        (
                            "Overwrite=No. Restoring normal "
                            "boot and leaving existing RAID "
                            "unchanged."
                        ),
                    )

                    server.reboot_normal()

                    return {
                        "row":
                            row_number,

                        "ip":
                            ip,

                        "status":
                            "Skipped",

                        "reason":
                            (
                                "Existing RAID found after "
                                "System Utilities boot "
                                f"via "
                                f"{inventory_source_after_boot}"
                            ),
                    }

        # =====================================================================
        # VALIDATE CONTROLLER
        # =====================================================================

        if not controllers:

            return {
                "row":
                    row_number,

                "ip":
                    ip,

                "status":
                    "Failed",

                "reason":
                    (
                        "Smart Array controller inventory "
                        "still unavailable after booting "
                        f"to System Utilities for "
                        f"{ctrl_timeout} mins"
                    ),
            }

        if not config_uri:

            return {
                "row":
                    row_number,

                "ip":
                    ip,

                "status":
                    "Failed",

                "reason":
                    (
                        "SmartStorageConfig still unavailable "
                        "after booting to System Utilities for "
                        f"{ctrl_timeout} mins"
                    ),
            }

        log(
            row_number,
            ip,
            (
                "SmartStorageConfig available: "
                f"{config_uri}"
            ),
        )

        log(
            row_number,
            ip,
            (
                "Physical drives exposed for "
                f"configuration: {drive_locations}"
            ),
        )

        # =====================================================================
        # DRIVE VALIDATION
        # =====================================================================

        if (
            len(drive_locations)
            < RAID_DATA_DRIVE_COUNT
        ):

            if booted_to_utilities:

                try:
                    server.reboot_normal()
                except Exception:
                    pass

            return {
                "row":
                    row_number,

                "ip":
                    ip,

                "status":
                    "Failed",

                "reason":
                    (
                        f"Only {len(drive_locations)} "
                        "physical drive(s) visible in "
                        "SmartStorageConfig; RAID1 requires 2"
                    ),
            }

        # =====================================================================
        # STAGE RAID1
        # =====================================================================

        selected_drives = (
            server.stage_raid1_configuration(
                config_uri,
                drive_locations,
            )
        )

        # =====================================================================
        # REBOOT TO APPLY
        #
        # SmartStorageConfig changes are pending settings and are applied
        # during reboot.
        # =====================================================================

        log(
            row_number,
            ip,
            (
                "RAID configuration staged. "
                "Rebooting server to apply "
                "Smart Array settings..."
            ),
        )

        server.reboot_normal()

        # =====================================================================
        # VERIFY
        # =====================================================================

        success = (
            server.poll_for_raid(
                baseline_count,
                raid_timeout,
            )
        )

        if success:

            return {
                "row":
                    row_number,

                "ip":
                    ip,

                "status":
                    "Successful",

                "reason":
                    (
                        "RAID1 created successfully "
                        f"on {', '.join(selected_drives)}"
                    ),
            }

        return {
            "row":
                row_number,

            "ip":
                ip,

            "status":
                "Failed",

            "reason":
                (
                    "Timeout waiting for RAID1 "
                    f"to appear after "
                    f"{raid_timeout} mins"
                ),
        }

    except Exception as exc:

        try:

            if booted_to_utilities:
                server.set_boot_to_normal()

        except Exception:

            pass

        return {
            "row":
                row_number,

            "ip":
                ip,

            "status":
                "Failed",

            "reason":
                str(exc),
        }

    finally:

        server.session.close()


# =============================================================================
# 6. MAIN
# =============================================================================

def main():

    excel_path = EXCEL_PATH

    if not os.path.exists(
        excel_path
    ):

        print(
            "ERROR: Could not find "
            f"Excel file at {excel_path}"
        )

        sys.exit(1)

    try:

        print(
            f"Loading data from "
            f"{excel_path} "
            f"(Sheet: '{SHEET_NAME}')..."
        )

        end_text = (
            END_ROW
            if END_ROW is not None
            else "end of data"
        )

        print(
            (
                "Excel row range: "
                f"{START_ROW} through "
                f"{end_text} (inclusive)"
            )
        )

        print(
            (
                "Optimized load enabled: "
                "within the selected range, "
                "reading stops after "
                f"{EXCEL_EMPTY_ROW_STOP} "
                "consecutive empty rows."
            )
        )

        df = (
            load_resource_excel_fast(
                excel_path,
                SHEET_NAME,
                START_ROW,
                END_ROW,
                EXCEL_EMPTY_ROW_STOP,
            )
        )

    except Exception as exc:

        print(
            f"Failed to read Excel file: {exc}"
        )

        sys.exit(1)

    if df.empty:

        print(
            "No populated rows found "
            "in selected range."
        )

        sys.exit(0)

    # -------------------------------------------------------------------------
    # Validate columns
    # -------------------------------------------------------------------------

    if (
        "equipment_type"
        not in df.columns
    ):

        print(
            "ERROR: 'equipment_type' "
            "column is missing."
        )

        sys.exit(1)

    missing_columns = [
        column
        for column
        in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        print(
            "ERROR: Missing required "
            "column(s): "
            + ", ".join(
                missing_columns
            )
        )

        sys.exit(1)

    # -------------------------------------------------------------------------
    # Equipment filter
    # -------------------------------------------------------------------------

    equipment_series = (
        df[
            "equipment_type"
        ]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df_filtered = df[
        equipment_series.isin(
            VALID_EQUIPMENT_TYPES
        )
    ].copy()

    if df_filtered.empty:

        print(
            "No matching servers found "
            "for equipment types: "
            + ", ".join(
                VALID_EQUIPMENT_TYPES
            )
        )

        sys.exit(0)

    servers_to_process = []
    final_report = []

    for _, row in (
        df_filtered.iterrows()
    ):

        excel_row = int(
            row[
                "_excel_row"
            ]
        )

        raw_ip = (
            row.get(
                "ilo_ip"
            )
        )

        ip = (
            str(
                raw_ip
            ).strip()
            if pd.notna(
                raw_ip
            )
            else "Unknown"
        )

        missing = [

            column

            for column
            in REQUIRED_COLUMNS

            if (
                column not in row
                or pd.isna(
                    row[
                        column
                    ]
                )
                or str(
                    row[
                        column
                    ]
                ).strip()
                == ""
            )
        ]

        if missing:

            final_report.append(
                {
                    "row":
                        excel_row,

                    "ip":
                        ip,

                    "status":
                        "Skipped",

                    "reason":
                        (
                            "Missing required value(s): "
                            + ", ".join(
                                missing
                            )
                        ),
                }
            )

            continue

        servers_to_process.append(
            {
                "excel_row":
                    excel_row,

                "ilo_ip":
                    ip,
            }
        )

    total_found = len(
        servers_to_process
    )

    print(
        "\nTotal valid DL380 Gen10+ "
        "servers found for processing: "
        f"{total_found}"
    )

    if total_found == 0:

        print(
            "No valid servers left "
            "to process."
        )

        sys.exit(0)

    user_input = input(
        "\nDo you want to OVERWRITE "
        "servers with already configured "
        "RAID volumes? (yes/no): "
    ).strip().lower()

    overwrite_raid = (
        user_input == "yes"
    )

    print(
        "\n"
        + "=" * 90
    )

    print(
        "STARTING PARALLEL "
        "DL380 GEN10+ RAID CONFIGURATION"
    )

    print(
        "Equipment types : "
        + ", ".join(
            VALID_EQUIPMENT_TYPES
        )
    )

    print(
        f"RAID level      : {RAID_LEVEL}"
    )

    print(
        f"Data drives     : "
        f"{RAID_DATA_DRIVE_COUNT}"
    )

    print(
        (
            "Overwrite RAID  : "
            + (
                "YES"
                if overwrite_raid
                else "NO"
            )
        )
    )

    print(
        f"Max workers     : {MAX_WORKERS}"
    )

    print(
        "=" * 90
    )

    safe_workers = min(
        MAX_WORKERS,
        total_found,
    )

    # =========================================================================
    # PARALLEL EXECUTION
    # =========================================================================

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=safe_workers
    ) as executor:

        futures = {

            executor.submit(
                process_server,
                server,
                overwrite_raid,
                CONTROLLER_TIMEOUT_MINUTES,
                RAID_TIMEOUT_MINUTES,
            ):
                (server, time.time())

            for server
            in servers_to_process
        }

        for future in (
            concurrent.futures
            .as_completed(
                futures
            )
        ):

            (
                server_data,
                submitted_at,
            ) = futures[
                future
            ]

            try:

                result = (
                    future.result()
                )

            except Exception as exc:

                result = {
                    "row":
                        server_data[
                            "excel_row"
                        ],

                    "ip":
                        server_data[
                            "ilo_ip"
                        ],

                    "status":
                        "Failed",

                    "reason":
                        (
                            "Unhandled worker exception: "
                            f"{exc}"
                        ),
                }

            result[
                "time_seconds"
            ] = round(
                time.time()
                - submitted_at,
                2,
            )

            final_report.append(
                result
            )

            log(
                result[
                    "row"
                ],
                result[
                    "ip"
                ],
                (
                    "FINISHED - Status: "
                    f"{result['status']}"
                ),
            )

    # =========================================================================
    # REPORT
    # =========================================================================

    final_report = sorted(
        final_report,
        key=lambda item:
            item[
                "row"
            ],
    )

    print(
        "\n\n"
        + "=" * 110
    )

    print(
        "FINAL EXECUTION REPORT: "
        "HPE DL380 Gen10+"
    )

    print(
        "=" * 110
    )

    print(
        f"{'ROW':<7} | "
        f"{'iLO IP ADDRESS':<16} | "
        f"{'STATUS':<12} | "
        f"REASON / DETAILS"
    )

    print(
        "-" * 110
    )

    for server_result in (
        final_report
    ):

        print(
            f"{server_result['row']:<7} | "
            f"{server_result['ip']:<16} | "
            f"{server_result['status']:<12} | "
            f"{server_result['reason']}"
        )

    print(
        "=" * 110
        + "\n"
    )

    # =========================================================================
    # CSV
    # =========================================================================

    if final_report:

        log_dir = LOG_DIR

        os.makedirs(
            log_dir,
            exist_ok=True,
        )

        timestamp = (
            time.strftime(
                "%Y%m%d-%H%M%S"
            )
        )

        range_text = (
            f"rows_{START_ROW}-"
            f"{END_ROW if END_ROW is not None else 'end'}"
        )

        report_filename = (
            f"{REPORT_PREFIX}_"
            f"{range_text}_"
            f"{timestamp}.csv"
        )

        report_path = (
            os.path.join(
                log_dir,
                report_filename,
            )
        )

        report_df = (
            pd.DataFrame(
                final_report
            )
        )

        report_df = report_df[
            [
                "row",
                "ip",
                "status",
                "time_seconds",
                "reason",
            ]
        ]

        report_df.to_csv(
            report_path,
            index=False,
        )

        print(
            "Detailed CSV saved to: "
            f"{report_path}\n"
        )


# =============================================================================
# ENTRY POINT
# =============================================================================

    summary_rows = [
        make_summary_row(
            row=item.get("row", "-"),
            item_type="RAID Rackmount",
            name="DL380 Gen10+",
            target=item.get("ip", ""),
            status=item.get("status", "Unknown"),
            time_seconds=item.get("time_seconds", 0.0),
            details=item.get("reason", ""),
        )
        for item in final_report
    ]

    print_summary_report(
        summary_rows,
        title="FINAL RAID RACK-MOUNT SUMMARY",
    )

    write_summary_csv(
        summary_rows,
        vars.SCRIPT_ARTIFACT_PREFIXES[
            "configure_raid_RM"
        ],
    )

    return (
        1
        if any(
            item.get("status") == "Failed"
            for item in final_report
        )
        else 0
    )


if __name__ == "__main__":

    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES[
                "configure_raid_RM"
            ],
            title="RACK-MOUNT RAID CONFIGURATION",
        )
    )