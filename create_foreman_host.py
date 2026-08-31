import sys

from functions import vars
from functions.output_log import run_logged_main
from functions.reporting import (
    foreman_summary_rows,
    print_summary_report,
    write_summary_csv,
)


def main():
    from functions.orchestrator import provision_from_excel

    print("Python executable : {}".format(sys.executable))
    print("Project directory : {}".format(vars.PROJECT_DIR))
    print("Templates directory: {}".format(vars.TEMPLATES_DIR))
    print("Resource list     : {}".format(vars.RESOURCE_LIST))
    print("Sheet             : {}".format(vars.SHEET_NAME))
    print("Rows              : {} through {}".format(
        vars.START_ROW,
        vars.END_ROW,
    ))
    print("Parallel workers  : {}".format(vars.MAX_WORKERS))
    print("Foreman creates   : {}".format(
        vars.FOREMAN_CREATE_CONCURRENCY
    ))
    print("Physical PXE boot : {}".format(
        (
            "ENABLED - auto start/reboot"
            if vars.FOREMAN_PHYSICAL_NETWORK_BOOT_ENABLED
            else "DISABLED"
        )
    ))
    print("PXE rack types    : {}".format(
        ", ".join(
            vars.FOREMAN_PHYSICAL_NETWORK_BOOT_RACK_TYPES
        )
    ))
    print("PXE blade types   : {}".format(
        ", ".join(
            vars.FOREMAN_PHYSICAL_NETWORK_BOOT_BLADE_TYPES
        )
    ))
    print()

    results = provision_from_excel()

    summary_rows = foreman_summary_rows(
        results
    )

    print_summary_report(
        summary_rows,
        title="FINAL FOREMAN PROVISIONING SUMMARY",
    )

    write_summary_csv(
        summary_rows,
        vars.SCRIPT_ARTIFACT_PREFIXES[
            "create_foreman_host"
        ],
    )

    failed = any(
        str(row.get("Status", "")).lower()
        in ("failed", "partial")
        for row in summary_rows
    )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES[
                "create_foreman_host"
            ],
            title="FOREMAN HOST PROVISIONING",
        )
    )
