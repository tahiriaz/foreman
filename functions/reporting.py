import csv
import os
from datetime import datetime

from functions import vars


SUMMARY_FIELDS = [
    "Row",
    "Type",
    "Name",
    "Target",
    "Status",
    "TimeSeconds",
    "Details",
]


def make_summary_row(
    row="-",
    item_type="",
    name="",
    target="",
    status="",
    time_seconds=0.0,
    details="",
):
    """Create one row using the project-wide summary schema."""
    try:
        elapsed = round(float(time_seconds), 2)
    except Exception:
        elapsed = 0.0

    return {
        "Row": row if row not in (None, "") else "-",
        "Type": str(item_type or ""),
        "Name": str(name or ""),
        "Target": str(target or ""),
        "Status": str(status or "Unknown"),
        "TimeSeconds": elapsed,
        "Details": str(details or ""),
    }


def _status_bucket(status):
    """Map script-specific statuses into common summary counters."""
    value = str(status or "").strip().lower()

    if not value:
        return "Other"

    if (
        "skip" in value
        or "missing cols" in value
        or "missing columns" in value
    ):
        return "Skipped"

    if (
        "partial" in value
        or "completed w/ errors" in value
        or "completed with errors" in value
    ):
        return "Partial"

    if (
        "fail" in value
        or "error" in value
        or "timeout" in value
    ):
        return "Failed"

    if value in (
        "successful",
        "success",
        "ok",
        "completed",
        "generated",
        "overwritten",
    ):
        return "Successful"

    return "Other"


def _summary_sort_key(item):
    row = item.get("Row", "-")

    try:
        return (0, int(row))
    except Exception:
        return (1, str(row))


def print_summary_report(
    results,
    title="FINAL SUMMARY REPORT",
):
    """Print the common console summary used by all main-folder scripts."""
    rows = list(results or [])
    rows.sort(key=_summary_sort_key)

    counts = {
        "Successful": 0,
        "Partial": 0,
        "Failed": 0,
        "Skipped": 0,
        "Other": 0,
    }

    for item in rows:
        bucket = _status_bucket(
            item.get("Status")
        )
        counts[bucket] += 1

    width = 170

    print("\n" + "=" * width)
    print(title)
    print("=" * width)
    print(
        "{:<9} | {:<22} | {:<28} | {:<24} | "
        "{:<18} | {:>9} | {}".format(
            "ROW",
            "TYPE",
            "NAME",
            "TARGET",
            "STATUS",
            "TIME (s)",
            "DETAILS",
        )
    )
    print("-" * width)

    for item in rows:
        details = str(
            item.get("Details", "")
        ).replace("\r", " ").replace("\n", " | ")

        try:
            elapsed = float(
                item.get("TimeSeconds", 0.0)
            )
        except Exception:
            elapsed = 0.0

        print(
            "{:<9} | {:<22} | {:<28} | {:<24} | "
            "{:<18} | {:>9.2f} | {}".format(
                str(item.get("Row", "-"))[:9],
                str(item.get("Type", ""))[:22],
                str(item.get("Name", ""))[:28],
                str(item.get("Target", ""))[:24],
                str(item.get("Status", "Unknown"))[:18],
                elapsed,
                details,
            )
        )

    print("=" * width)
    print(
        "TOTAL: {} | SUCCESSFUL: {} | PARTIAL: {} | "
        "FAILED: {} | SKIPPED: {} | OTHER: {}".format(
            len(rows),
            counts["Successful"],
            counts["Partial"],
            counts["Failed"],
            counts["Skipped"],
            counts["Other"],
        )
    )
    print("=" * width + "\n")

    return counts


def write_summary_csv(
    results,
    report_prefix,
    log_dir=None,
):
    """Write the common seven-column summary CSV and return its path."""
    if log_dir is None:
        log_dir = vars.LOG_DIR

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = os.path.join(
        log_dir,
        "{}_Summary_{}.csv".format(
            report_prefix,
            timestamp,
        ),
    )

    rows = list(results or [])
    rows.sort(key=_summary_sort_key)

    with open(
        report_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=SUMMARY_FIELDS,
            extrasaction="ignore",
        )
        writer.writeheader()

        for item in rows:
            writer.writerow({
                field: item.get(field, "")
                for field in SUMMARY_FIELDS
            })

    print("Summary CSV saved to: {}".format(report_path))
    return report_path


def foreman_summary_rows(results):
    """Convert Foreman orchestrator results to the common summary schema."""
    summary = []

    for result in results or []:
        component_details = (
            "Foreman={}; DNS={}; Ansible={}".format(
                result.get("Foreman", "N/A"),
                result.get("DNS", "N/A"),
                result.get("Ansible", "N/A"),
            )
        )

        details = str(
            result.get("Details", "")
        ).strip()

        if details:
            component_details += "; " + details

        summary.append(
            make_summary_row(
                row=result.get("ExcelRow", "-"),
                item_type=result.get("EquipmentType", ""),
                name=result.get("LogicalName", ""),
                target=vars.FOREMAN_URL,
                status=result.get("Status", "Unknown"),
                time_seconds=result.get("TimeSeconds", 0.0),
                details=component_details,
            )
        )

    return summary


def print_final_report(results):
    """Compatibility wrapper for the Foreman provisioning workflow."""
    return print_summary_report(
        foreman_summary_rows(results),
        title="FINAL FOREMAN PROVISIONING SUMMARY",
    )
