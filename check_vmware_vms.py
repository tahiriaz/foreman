# BUILD_MARKER: CHECK_VMWARE_VMS_NAME_IP_V2_20260830

import os
import sys
import time
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

import pandas as pd

from functions import vars
from functions.output_log import run_logged_main
from functions.reporting import (
    make_summary_row,
    print_summary_report,
    write_summary_csv,
)
from functions.vmware_inventory import (
    VCenterClient,
    build_vm_ip_index,
    build_vm_name_index,
    check_record,
)


def _normalized_column_map(
    columns,
):

    result = {}

    for column in columns:

        normalized = str(
            column
        ).strip().lower()

        if normalized:

            result[
                normalized
            ] = column

    return result


def _cell_value(
    row,
    column,
):

    value = row.get(
        column
    )

    if pd.isna(
        value
    ):

        return vars.EMPTY_VALUE

    return value


def load_virtual_machine_rows():
    """
    Read exactly vars.START_ROW through vars.END_ROW, inclusive.

    Required worksheet columns:
      equipment_type
      hostname
      logical_name
      fe_ip_address
      me_ip_address

    fe_ip_address must be populated for every Virtual Machine row.
    me_ip_address may be blank.
    """

    if vars.START_ROW < 2:

        raise ValueError(
            "START_ROW must be >= 2 because Excel row 1 "
            "contains the column headers."
        )

    if vars.END_ROW < vars.START_ROW:

        raise ValueError(
            "END_ROW cannot be less than START_ROW."
        )

    if not os.path.isfile(
        vars.RESOURCE_LIST
    ):

        raise FileNotFoundError(
            "Excel resource list was not found: {}".format(
                vars.RESOURCE_LIST
            )
        )

    print(
        "Loading VMware VM check inventory from "
        "{} (Sheet: '{}')...".format(
            vars.RESOURCE_LIST,
            vars.SHEET_NAME,
        )
    )

    print(
        "Excel row range: {} through {} (inclusive)"
        .format(
            vars.START_ROW,
            vars.END_ROW,
        )
    )

    frame = pd.read_excel(
        vars.RESOURCE_LIST,
        sheet_name=vars.SHEET_NAME,
        skiprows=range(
            1,
            vars.START_ROW - 1,
        ),
        nrows=(
            vars.END_ROW
            - vars.START_ROW
            + 1
        ),
        engine=vars.EXCEL_ENGINE,
    )

    column_map = (
        _normalized_column_map(
            frame.columns
        )
    )

    missing = [
        column
        for column
        in vars.VMWARE_REQUIRED_COLUMNS
        if column.lower()
        not in column_map
    ]

    if missing:

        raise ValueError(
            "Required Excel column(s) are missing: {}. "
            "Required columns: {}"
            .format(
                ", ".join(
                    missing
                ),
                ", ".join(
                    vars.VMWARE_REQUIRED_COLUMNS
                ),
            )
        )

    rename_map = {}

    for required in (
        vars.VMWARE_REQUIRED_COLUMNS
    ):

        actual = (
            column_map[
                required.lower()
            ]
        )

        if actual != required:

            rename_map[
                actual
            ] = required

    if rename_map:

        frame = frame.rename(
            columns=rename_map
        )

    records = []

    for position, row in frame.iterrows():

        excel_row = (
            vars.START_ROW
            + int(
                position
            )
        )

        equipment_type = str(
            _cell_value(
                row,
                "equipment_type",
            )
            or ""
        ).strip()

        if (
            equipment_type.lower()
            != vars
            .VMWARE_EQUIPMENT_TYPE
            .lower()
        ):

            continue

        records.append({
            "equipment_type":
                equipment_type,

            "hostname":
                _cell_value(
                    row,
                    "hostname",
                ),

            "logical_name":
                _cell_value(
                    row,
                    "logical_name",
                ),

            "fe_ip_address":
                _cell_value(
                    row,
                    "fe_ip_address",
                ),

            "me_ip_address":
                _cell_value(
                    row,
                    "me_ip_address",
                ),

            "_excel_row":
                excel_row,
        })

    return records


def _display_name(
    record,
):

    logical_name = str(
        record.get(
            "logical_name",
            "",
        )
        or ""
    ).strip()

    hostname = str(
        record.get(
            "hostname",
            "",
        )
        or ""
    ).strip()

    invalid = {
        str(
            value
        ).strip().upper()
        for value in vars.INVALID_VALUES
    }

    if (
        logical_name
        and logical_name.upper()
        not in invalid
    ):

        return logical_name

    if (
        hostname
        and hostname.upper()
        not in invalid
    ):

        return hostname

    return "Unknown"


def check_one_record(
    record,
    vm_name_index,
    vm_ip_index,
    ip_scan_info,
):

    started = time.time()

    excel_row = (
        record.get(
            "_excel_row",
            "-",
        )
    )

    name = (
        _display_name(
            record
        )
    )

    try:

        check = check_record(
            record,
            vm_name_index,
            vm_ip_index,
            ip_scan_info,
        )

        if not check.get(
            "valid"
        ):

            status = "Failed"

        elif (
            vars.VMWARE_REQUIRE_COMPLETE_IP_INVENTORY
            and not check.get(
                "ip_inventory_complete",
                True,
            )
            and not check.get(
                "fe_ip_conflict"
            )
            and not check.get(
                "me_ip_conflict"
            )
        ):

            # No detected IP conflict is not conclusive if some existing VMs
            # could not be inspected for guest IP data.
            status = "Partial"

        else:

            status = "Successful"

        details = (
            check.get(
                "details",
                "",
            )
        )

        print(
            "[Row {} | {}] {}"
            .format(
                excel_row,
                name,
                details,
            )
        )

        return (
            make_summary_row(
                row=excel_row,
                item_type=(
                    "VMware VM Check"
                ),
                name=name,
                target=vars.VMWARE_HOST,
                status=status,
                time_seconds=(
                    time.time()
                    - started
                ),
                details=details,
            ),
            check,
        )

    except Exception as exc:

        details = (
            "VM name/IP existence check failed: {}"
            .format(
                exc
            )
        )

        print(
            "[Row {} | {}] FAILED - {}"
            .format(
                excel_row,
                name,
                details,
            )
        )

        return (
            make_summary_row(
                row=excel_row,
                item_type=(
                    "VMware VM Check"
                ),
                name=name,
                target=vars.VMWARE_HOST,
                status="Failed",
                time_seconds=(
                    time.time()
                    - started
                ),
                details=details,
            ),
            {
                "checked":
                    False,

                "valid":
                    False,

                "name_exists":
                    False,

                "fe_ip_conflict":
                    False,

                "me_ip_conflict":
                    False,

                "any_conflict":
                    False,
            },
        )


def main():

    print(
        "Python executable : {}".format(
            sys.executable
        )
    )

    print(
        "Project directory : {}".format(
            vars.PROJECT_DIR
        )
    )

    print(
        "Templates directory: {}".format(
            vars.TEMPLATES_DIR
        )
    )

    print(
        "Resource list     : {}".format(
            vars.RESOURCE_LIST
        )
    )

    print(
        "Sheet             : {}".format(
            vars.SHEET_NAME
        )
    )

    print(
        "Rows              : {} through {}"
        .format(
            vars.START_ROW,
            vars.END_ROW,
        )
    )

    print(
        "Equipment type    : {}".format(
            vars.VMWARE_EQUIPMENT_TYPE
        )
    )

    print(
        "Required columns  : {}".format(
            ", ".join(
                vars.VMWARE_REQUIRED_COLUMNS
            )
        )
    )

    print(
        "FE IP required    : {}".format(
            (
                "YES"
                if vars.VMWARE_FE_IP_REQUIRED
                else "NO"
            )
        )
    )

    print(
        "ME IP empty       : ALLOWED"
    )

    print(
        "vCenter           : {}".format(
            vars.VMWARE_HOST
        )
    )

    print(
        "Row check workers : {}".format(
            vars.VMWARE_CHECK_MAX_WORKERS
        )
    )

    print(
        "IP lookup workers : {}".format(
            vars.VMWARE_IP_LOOKUP_MAX_WORKERS
        )
    )

    print()

    records = (
        load_virtual_machine_rows()
    )

    print(
        "Virtual Machine rows found in selected range: {}"
        .format(
            len(
                records
            )
        )
    )

    if not records:

        print(
            "No equipment_type='{}' rows were found. "
            "Nothing to check."
            .format(
                vars.VMWARE_EQUIPMENT_TYPE
            )
        )

        print_summary_report(
            [],
            title=(
                "FINAL VMWARE VM NAME / IP CHECK SUMMARY"
            ),
        )

        write_summary_csv(
            [],
            vars.VMWARE_REPORT_PREFIX,
            log_dir=vars.LOG_DIR,
        )

        return 0

    client = (
        VCenterClient()
    )

    try:

        print(
            "\nConnecting to vCenter {}..."
            .format(
                vars.VMWARE_HOST
            )
        )

        client.login()

        print(
            "Connected successfully using vCenter REST API "
            "mode '{}'."
            .format(
                client.api_mode
            )
        )

        print(
            "Retrieving vCenter VM inventory..."
        )

        vm_list = (
            client.list_vms()
        )

        print(
            "VM objects returned by vCenter: {}"
            .format(
                len(
                    vm_list
                )
            )
        )

        vm_name_index = (
            build_vm_name_index(
                vm_list
            )
        )

        print(
            "Unique case-insensitive VM names indexed: {}"
            .format(
                len(
                    vm_name_index
                )
            )
        )

        print(
            "\nRetrieving guest IP addresses from vCenter "
            "in parallel..."
        )

        (
            vm_ip_index,
            ip_scan_info,
        ) = (
            build_vm_ip_index(
                client,
                vm_list,
                vars.VMWARE_IP_LOOKUP_MAX_WORKERS,
            )
        )

        print(
            "Guest IP inventory: "
            "VMs={} | Readable={} | Unavailable={} | "
            "Errors={} | UniqueIPs={} | Complete={}"
            .format(
                ip_scan_info[
                    "total_vms"
                ],
                ip_scan_info[
                    "available_vms"
                ],
                ip_scan_info[
                    "unavailable_vms"
                ],
                ip_scan_info[
                    "error_vms"
                ],
                ip_scan_info[
                    "unique_ips"
                ],
                (
                    "YES"
                    if ip_scan_info[
                        "complete"
                    ]
                    else "NO"
                ),
            )
        )

        if not ip_scan_info[
            "complete"
        ]:

            print(
                "WARNING: Guest IP inventory is incomplete. "
                "VMware Tools/guest networking data was unavailable "
                "for one or more existing VMs. Rows without a "
                "detected IP conflict will be marked Partial."
            )

    finally:

        client.close()

    print(
        "\nStarting parallel Excel-to-vCenter "
        "name and reserved-IP checks..."
    )

    summary_rows = []
    checks = []

    with ThreadPoolExecutor(
        max_workers=(
            vars.VMWARE_CHECK_MAX_WORKERS
        )
    ) as executor:

        future_map = {
            executor.submit(
                check_one_record,
                record,
                vm_name_index,
                vm_ip_index,
                ip_scan_info,
            ):
                record
            for record in records
        }

        for future in as_completed(
            future_map
        ):

            summary_row, check = (
                future.result()
            )

            summary_rows.append(
                summary_row
            )

            checks.append(
                check
            )

    name_exists_count = sum(
        1
        for check in checks
        if check.get(
            "name_exists"
        )
    )

    fe_conflict_count = sum(
        1
        for check in checks
        if check.get(
            "fe_ip_conflict"
        )
    )

    me_conflict_count = sum(
        1
        for check in checks
        if check.get(
            "me_ip_conflict"
        )
    )

    any_conflict_count = sum(
        1
        for check in checks
        if check.get(
            "any_conflict"
        )
    )

    failed_count = sum(
        1
        for row in summary_rows
        if "fail"
        in str(
            row.get(
                "Status",
                "",
            )
        ).lower()
    )

    partial_count = sum(
        1
        for row in summary_rows
        if "partial"
        in str(
            row.get(
                "Status",
                "",
            )
        ).lower()
    )

    print(
        "\nVM NAME / RESERVED-IP RESULT: "
        "ROWS={} | NAME EXISTS={} | FE IP CONFLICT={} | "
        "ME IP CONFLICT={} | ANY CONFLICT={} | "
        "PARTIAL={} | FAILED={}"
        .format(
            len(
                records
            ),
            name_exists_count,
            fe_conflict_count,
            me_conflict_count,
            any_conflict_count,
            partial_count,
            failed_count,
        )
    )

    print_summary_report(
        summary_rows,
        title=(
            "FINAL VMWARE VM NAME / IP CHECK SUMMARY"
        ),
    )

    write_summary_csv(
        summary_rows,
        vars.VMWARE_REPORT_PREFIX,
        log_dir=vars.LOG_DIR,
    )

    return (
        1
        if failed_count
        else 0
    )


if __name__ == "__main__":

    prefix = (
        vars.SCRIPT_ARTIFACT_PREFIXES.get(
            "check_vmware_vms",
            vars.VMWARE_REPORT_PREFIX,
        )
    )

    sys.exit(
        run_logged_main(
            main,
            log_prefix=prefix,
            title=(
                "VMWARE VM NAME / IP CHECK"
            ),
            log_dir=vars.LOG_DIR,
        )
    )
