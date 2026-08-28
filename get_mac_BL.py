# BUILD_MARKER: GET_MAC_BL_CENTRAL_V1_20260828

import gc
import os
import re
import time
import warnings

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    message=".*Python 3.6 is no longer supported.*",
)
warnings.filterwarnings(
    "ignore",
    module="cryptography",
)
warnings.filterwarnings(
    "ignore",
    module="paramiko",
)

import paramiko
import win32com.client as win32
from openpyxl import load_workbook

from functions import vars
from functions.output_log import run_logged_main
from functions.reporting import (
    make_summary_row,
    print_summary_report,
    write_summary_csv,
)


# ============================================================================
# OA CONNECTION
# ============================================================================

class OAConnection:
    """Interactive SSH connection wrapper for HPE Onboard Administrator."""

    def __init__(
        self,
        primary_ip,
        secondary_ip,
        user,
        password,
    ):
        self.ips = [
            ip
            for ip
            in (
                primary_ip,
                secondary_ip,
            )
            if ip
        ]

        self.user = user
        self.password = password

        self.ssh = None
        self.channel = None
        self.active_ip = None

    def connect(self):
        for ip in self.ips:
            print(
                "\nAttempting connection to OA at {}..."
                .format(
                    ip
                )
            )

            self.ssh = (
                paramiko.SSHClient()
            )

            self.ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )

            try:
                self.ssh.connect(
                    hostname=ip,
                    username=self.user,
                    password=self.password,
                    look_for_keys=False,
                    allow_agent=False,
                    timeout=(
                        vars.MAC_BL_OA_CONNECT_TIMEOUT
                    ),
                    banner_timeout=(
                        vars.MAC_BL_OA_BANNER_TIMEOUT
                    ),
                    auth_timeout=(
                        vars.MAC_BL_OA_AUTH_TIMEOUT
                    ),
                )

                transport = (
                    self.ssh.get_transport()
                )

                if transport:
                    transport.set_keepalive(
                        vars.MAC_BL_OA_KEEPALIVE_INTERVAL
                    )

                self.channel = (
                    self.ssh.invoke_shell()
                )

                time.sleep(
                    vars.MAC_BL_OA_SHELL_SETTLE_SECONDS
                )

                self._drain_channel()

                status_output = (
                    self.send_command(
                        "SHOW OA STATUS"
                    )
                )

                if re.search(
                    r"Role:\s*Active",
                    status_output,
                    flags=re.IGNORECASE,
                ):
                    print(
                        "Successfully connected to "
                        "ACTIVE OA ({})."
                        .format(
                            ip
                        )
                    )

                    self.active_ip = ip

                    return True

                print(
                    "OA at {} is standby/inactive. "
                    "Closing and trying next..."
                    .format(
                        ip
                    )
                )

                self.close()

            except Exception as exc:
                print(
                    "Failed to connect to {}: {}"
                    .format(
                        ip,
                        exc,
                    )
                )

                self.close()

        return False

    def _drain_channel(self):
        output = ""

        while (
            self.channel
            and self.channel.recv_ready()
        ):
            data = (
                self.channel.recv(
                    65535
                )
            )

            if not data:
                break

            output += data.decode(
                "utf-8",
                errors="replace",
            )

        return output

    def send_command(
        self,
        command,
        wait_string=">",
    ):
        """Send one OA command and return the complete interactive output."""
        if not self.channel:
            return ""

        self._drain_channel()

        self.channel.send(
            command + "\n"
        )

        output = ""

        deadline = (
            time.time()
            + vars.MAC_BL_OA_COMMAND_TIMEOUT_SECONDS
        )

        while (
            time.time()
            < deadline
        ):
            if self.channel.recv_ready():
                data = (
                    self.channel.recv(
                        65535
                    )
                )

                if not data:
                    break

                text = data.decode(
                    "utf-8",
                    errors="replace",
                )

                output += text

                lower_text = (
                    text.lower()
                )

                if (
                    "any key"
                    in lower_text
                    or "more"
                    in lower_text
                ):
                    self.channel.send(
                        " "
                    )

                if (
                    wait_string
                    in output
                ):
                    time.sleep(
                        vars.MAC_BL_OA_COMMAND_SETTLE_SECONDS
                    )

                    output += (
                        self._drain_channel()
                    )

                    break

            else:
                time.sleep(
                    vars.MAC_BL_OA_POLL_INTERVAL_SECONDS
                )

        return output

    def close(self):
        if self.channel:
            try:
                self.channel.close()
            except Exception:
                pass

        self.channel = None

        if self.ssh:
            try:
                self.ssh.close()
            except Exception:
                pass

        self.ssh = None


# ============================================================================
# HELPERS
# ============================================================================

def check_file_writable(file_path):
    if not os.path.exists(
        file_path
    ):
        return True

    try:
        with open(
            file_path,
            "a+",
        ):
            pass

        return True

    except PermissionError:
        return False


def get_all_enclosure_details(
    oa_connection,
):
    """Fetch serial numbers and MAC addresses for every blade in one enclosure."""
    results = {}

    print(
        "Fetching global serial numbers for all blades..."
    )

    info_raw = (
        oa_connection.send_command(
            "SHOW SERVER INFO ALL"
        )
    )

    print(
        "Fetching global port maps for all blades..."
    )

    port_raw = (
        oa_connection.send_command(
            "SHOW SERVER PORT MAP ALL"
        )
    )

    bay_regex = re.compile(
        r"(?:Server\s+)?Blade\s*"
        r"(?:#|Number)?\s*(\d+)",
        re.IGNORECASE,
    )

    current_bay = None

    for line in info_raw.splitlines():
        bay_match = (
            bay_regex.search(
                line
            )
        )

        if bay_match:
            current_bay = int(
                bay_match.group(
                    1
                )
            )

            if (
                current_bay
                not in results
            ):
                results[
                    current_bay
                ] = {
                    "serial": (
                        "Serial Number not found"
                    ),
                    "macs": (
                        [""]
                        * vars.MAC_MAX_ADDRESSES
                    ),
                }

        if current_bay:
            serial_match = re.search(
                r"Serial Number:\s*"
                r"([A-Za-z0-9\-]+)",
                line,
                re.IGNORECASE,
            )

            if serial_match:
                results[
                    current_bay
                ][
                    "serial"
                ] = (
                    serial_match.group(
                        1
                    ).strip()
                )

    current_bay = None
    current_section = "other"

    flb_macs = {}
    other_macs = {}

    mac_pattern = re.compile(
        r"(?:[0-9A-Fa-f]{2}[:-]){5}"
        r"[0-9A-Fa-f]{2}"
    )

    for line in port_raw.splitlines():
        bay_match = (
            bay_regex.search(
                line
            )
        )

        if bay_match:
            current_bay = int(
                bay_match.group(
                    1
                )
            )

            if (
                current_bay
                not in flb_macs
            ):
                flb_macs[
                    current_bay
                ] = []

                other_macs[
                    current_bay
                ] = []

            current_section = "other"

            continue

        if not current_bay:
            continue

        upper_line = (
            line.upper()
        )

        if (
            "LOM"
            in upper_line
            or "FLB"
            in upper_line
        ):
            current_section = "flb"

        elif (
            "MEZZ"
            in upper_line
        ):
            current_section = "other"

        for mac in (
            mac_pattern.findall(
                line
            )
        ):
            clean_mac = (
                mac.replace(
                    "-",
                    ":",
                ).upper()
            )

            if current_section == "flb":
                if (
                    clean_mac
                    not in flb_macs[
                        current_bay
                    ]
                ):
                    flb_macs[
                        current_bay
                    ].append(
                        clean_mac
                    )

            else:
                if (
                    clean_mac
                    not in other_macs[
                        current_bay
                    ]
                ):
                    other_macs[
                        current_bay
                    ].append(
                        clean_mac
                    )

    for bay, flb_list in (
        flb_macs.items()
    ):
        if bay not in results:
            results[
                bay
            ] = {
                "serial": (
                    "Serial Number not found"
                ),
                "macs": (
                    [""]
                    * vars.MAC_MAX_ADDRESSES
                ),
            }

        other_list = (
            other_macs.get(
                bay,
                [],
            )
        )

        combined = (
            flb_list
            + [
                mac
                for mac
                in other_list
                if mac not in flb_list
            ]
        )

        for index in range(
            min(
                len(
                    combined
                ),
                vars.MAC_MAX_ADDRESSES,
            )
        ):
            results[
                bay
            ][
                "macs"
            ][
                index
            ] = combined[
                index
            ]

    return results


def refresh_excel_formulas(
    file_path,
):
    """Ask native Excel to rebuild cached formula values."""
    print(
        "\nCommanding Excel to recalculate formulas "
        "in the background..."
    )

    absolute_path = (
        os.path.abspath(
            file_path
        )
    )

    excel = None
    workbook = None

    try:
        excel = win32.DispatchEx(
            "Excel.Application"
        )

        excel.Visible = False
        excel.DisplayAlerts = False

        workbook = (
            excel.Workbooks.Open(
                absolute_path
            )
        )

        workbook.Save()

        print(
            "Formula cache successfully rebuilt!"
        )

    except Exception as exc:
        print(
            "WARNING: Could not trigger Excel to "
            "rebuild formulas: {}".format(
                exc
            )
        )

    finally:
        if workbook:
            try:
                workbook.Close(
                    SaveChanges=False
                )
            except Exception:
                pass

        if excel:
            try:
                excel.Quit()
            except Exception:
                pass

        del workbook
        del excel

        gc.collect()


def scan_excel_for_blades(
    excel_path,
    sheet_name,
    enclosure_name,
):
    """
    Find the selected enclosure's OAs and blade rows using read-only Excel I/O.
    """
    print(
        "\nScanning Excel file "
        "(Fast Read-Only Mode)..."
    )

    workbook = load_workbook(
        excel_path,
        data_only=True,
        read_only=True,
    )

    try:
        if (
            sheet_name
            not in workbook.sheetnames
        ):
            return (
                None,
                "Error: Sheet '{}' not found."
                .format(
                    sheet_name
                ),
            )

        worksheet = (
            workbook[
                sheet_name
            ]
        )

        header_row = next(
            worksheet.iter_rows(
                min_row=1,
                max_row=1,
                values_only=True,
            ),
            None,
        )

        if not header_row:
            return (
                None,
                "Error: Excel header row is empty.",
            )

        headers = {}

        for index, cell_value in enumerate(
            header_row,
            1,
        ):
            if cell_value:
                headers[
                    str(
                        cell_value
                    ).strip()
                ] = index

        missing_columns = [
            column
            for column
            in vars.MAC_BL_REQUIRED_COLUMNS
            if column not in headers
        ]

        if missing_columns:
            return (
                None,
                "Error: Required columns missing: {}"
                .format(
                    ", ".join(
                        missing_columns
                    )
                ),
            )

        blade_rows = []

        primary_oa_ip = None
        secondary_oa_ip = None
        empty_count = 0

        for row_idx, row_values in enumerate(
            worksheet.iter_rows(
                min_row=2,
                values_only=True,
            ),
            2,
        ):
            if not any(
                row_values
            ):
                empty_count += 1

                if (
                    empty_count
                    >= vars.MAC_BL_EXCEL_EMPTY_ROW_STOP
                ):
                    break

                continue

            empty_count = 0

            enclosure_value = row_values[
                headers[
                    "enclosure_physical_name"
                ] - 1
            ]

            equipment_physical_value = (
                row_values[
                    headers[
                        "equipment_physical_name"
                    ] - 1
                ]
            )

            equipment_type_value = (
                row_values[
                    headers[
                        "equipment_type"
                    ] - 1
                ]
            )

            slot_value = row_values[
                headers[
                    "enclosure_slot"
                ] - 1
            ]

            ip_value = row_values[
                headers[
                    "ilo_ip"
                ] - 1
            ]

            enclosure_text = (
                str(
                    enclosure_value
                ).strip().upper()
                if enclosure_value
                else ""
            )

            equipment_physical_text = (
                str(
                    equipment_physical_value
                ).strip().upper()
                if equipment_physical_value
                else ""
            )

            is_match = (
                enclosure_text
                == enclosure_name
            )

            if (
                not is_match
                and len(
                    enclosure_name
                ) >= 14
                and equipment_physical_text.startswith(
                    enclosure_name[
                        :14
                    ]
                )
            ):
                is_match = True

            if not is_match:
                continue

            equipment_type = str(
                equipment_type_value
                or ""
            ).strip().upper()

            try:
                slot_number = int(
                    float(
                        str(
                            slot_value
                        ).strip()
                    )
                )

            except (
                ValueError,
                TypeError,
            ):
                slot_number = None

            if (
                "ENCLOSURE OA"
                in equipment_type
                and ip_value
            ):
                if slot_number == 1:
                    primary_oa_ip = str(
                        ip_value
                    ).strip()

                elif slot_number == 2:
                    secondary_oa_ip = str(
                        ip_value
                    ).strip()

            elif (
                "BLADE SERVER"
                in equipment_type
            ):
                blade_rows.append({
                    "row_idx": row_idx,
                    "slot": slot_number,
                    "eq_type": equipment_type,
                })

        return (
            (
                primary_oa_ip,
                secondary_oa_ip,
                blade_rows,
                headers,
            ),
            None,
        )

    finally:
        workbook.close()


# ============================================================================
# MAIN
# ============================================================================

def main():
    enclosure_name = input(
        "Enter the Enclosure Name: "
    ).strip().upper()

    excel_path = (
        vars.RESOURCE_LIST
    )

    sheet_name = (
        vars.SHEET_NAME
    )

    if not check_file_writable(
        excel_path
    ):
        print(
            "\nERROR: '{}' is currently open "
            "in Excel.".format(
                excel_path
            )
        )

        print(
            "Please close the file and run the script "
            "again to prevent permission errors."
        )

        return

    result, error = (
        scan_excel_for_blades(
            excel_path,
            sheet_name,
            enclosure_name,
        )
    )

    if error:
        print(
            error
        )

        return

    (
        primary_oa_ip,
        secondary_oa_ip,
        blade_rows,
        headers,
    ) = result

    if (
        not primary_oa_ip
        and not secondary_oa_ip
    ):
        print(
            "Error: Could not find OA IPs for "
            "Enclosure '{}'."
            .format(
                enclosure_name
            )
        )

        return

    if not blade_rows:
        print(
            "No Blade Servers found for "
            "Enclosure '{}'."
            .format(
                enclosure_name
            )
        )

        return

    print(
        "Found Primary OA: {} | "
        "Secondary OA: {}"
        .format(
            primary_oa_ip,
            secondary_oa_ip,
        )
    )

    print(
        "Found {} Blade Server(s) "
        "in this enclosure."
        .format(
            len(
                blade_rows
            )
        )
    )

    oa = OAConnection(
        primary_oa_ip,
        secondary_oa_ip,
        vars.OA_USERNAME,
        vars.OA_PASSWORD,
    )

    if not oa.connect():
        return

    hardware_data = {}

    try:
        hardware_data = (
            get_all_enclosure_details(
                oa
            )
        )

    finally:
        oa.close()

        print(
            "SSH connection closed."
        )

    print(
        "\nLoading Excel file "
        "(Writing Mode) to inject data..."
    )

    workbook_write = load_workbook(
        excel_path
    )

    worksheet_write = (
        workbook_write[
            sheet_name
        ]
    )

    summary_rows = []

    for blade in blade_rows:
        item_start = time.time()
        row_idx = blade[
            "row_idx"
        ]

        bay_number = blade[
            "slot"
        ]

        equipment_type = blade[
            "eq_type"
        ]

        print(
            "\n--- Processing Row {}: {} "
            "(Bay {}) ---"
            .format(
                row_idx,
                equipment_type,
                bay_number,
            )
        )

        if bay_number is None:
            print(
                "WARNING: Skipping blade at row {}. "
                "Missing or invalid enclosure_slot."
                .format(
                    row_idx
                )
            )

            summary_rows.append(
                make_summary_row(
                    row=row_idx,
                    item_type=equipment_type,
                    name="Unknown bay",
                    target=enclosure_name,
                    status="Skipped",
                    time_seconds=time.time() - item_start,
                    details="Missing or invalid enclosure_slot",
                )
            )

            continue

        bay_data = (
            hardware_data.get(
                bay_number,
                {
                    "serial": (
                        "Data not found"
                    ),
                    "macs": (
                        [""]
                        * vars.MAC_MAX_ADDRESSES
                    ),
                },
            )
        )

        serial_no = (
            bay_data[
                "serial"
            ]
        )

        macs = (
            bay_data[
                "macs"
            ]
        )

        worksheet_write.cell(
            row=row_idx,
            column=headers[
                vars.MAC_SERIAL_COLUMN
            ],
        ).value = serial_no

        for index, column_name in enumerate(
            vars.MAC_NIC_COLUMNS
        ):
            worksheet_write.cell(
                row=row_idx,
                column=headers[
                    column_name
                ],
            ).value = macs[
                index
            ]

        print(
            "  Serial Number : {}"
            .format(
                serial_no
            )
        )

        for index, mac in enumerate(
            macs,
            1,
        ):
            if not mac:
                print(
                    "  mac{}          : [MISSING]"
                    .format(
                        index
                    )
                )

            else:
                print(
                    "  mac{}          : {}"
                    .format(
                        index,
                        mac,
                    )
                )

        found_count = len([mac for mac in macs if mac])

        if (
            serial_no in ("Data not found", "Serial Number not found")
            or found_count < vars.MAC_MAX_ADDRESSES
        ):
            summary_status = "Partial"
        else:
            summary_status = "Successful"

        summary_rows.append(
            make_summary_row(
                row=row_idx,
                item_type=equipment_type,
                name="Bay {:02}".format(bay_number),
                target=enclosure_name,
                status=summary_status,
                time_seconds=time.time() - item_start,
                details=(
                    "Serial={}; MACs={}/{}; ActiveOA={}"
                    .format(
                        serial_no,
                        found_count,
                        vars.MAC_MAX_ADDRESSES,
                        oa.active_ip or "Unknown",
                    )
                ),
            )
        )

    print(
        "\nSaving updates to {}..."
        .format(
            excel_path
        )
    )

    workbook_write.save(
        excel_path
    )

    workbook_write.close()

    print(
        "Excel file successfully updated!"
    )

    refresh_excel_formulas(
        excel_path
    )

    print_summary_report(
        summary_rows,
        title="FINAL BLADE MAC COLLECTION SUMMARY",
    )

    write_summary_csv(
        summary_rows,
        vars.SCRIPT_ARTIFACT_PREFIXES[
            "get_mac_BL"
        ],
    )

    return (
        1
        if any(
            row["Status"] in ("Failed", "Partial")
            for row in summary_rows
        )
        else 0
    )


if __name__ == "__main__":
    import sys

    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES[
                "get_mac_BL"
            ],
            title="BLADE MAC COLLECTION",
        )
    )
