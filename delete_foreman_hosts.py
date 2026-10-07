import sys
import time

from functions import foreman, vars
from functions.output_log import run_logged_main
from functions.reporting import (
    make_summary_row,
    print_summary_report,
    write_summary_csv,
)


HOSTS_TO_DELETE = [
    "tvsnvrapp{:03d}mp.mak.iss".format(number)
    for number in range(65, 73)
]


def main():
    print("Foreman URL       : {}".format(vars.FOREMAN_URL))
    print("Hosts to consider : {}".format(len(HOSTS_TO_DELETE)))
    for hostname in HOSTS_TO_DELETE:
        print("  - {}".format(hostname))

    print("\nLooking up all requested hosts before making changes...")
    report = []
    hosts_found = []
    lookup_failed = False

    for hostname in HOSTS_TO_DELETE:
        started_at = time.time()
        try:
            host = foreman.get_host(hostname)
        except Exception as exc:
            lookup_failed = True
            report.append(
                make_summary_row(
                    item_type="Foreman Host",
                    name=hostname,
                    target=vars.FOREMAN_URL,
                    status="Failed",
                    time_seconds=time.time() - started_at,
                    details="Lookup failed: {}".format(exc),
                )
            )
            print("Lookup failed for {}: {}".format(hostname, exc))
            continue

        if host is None:
            report.append(
                make_summary_row(
                    item_type="Foreman Host",
                    name=hostname,
                    target=vars.FOREMAN_URL,
                    status="Not Found",
                    details="No exact Foreman host match; nothing to delete.",
                )
            )
            print("{}: not found; nothing to delete.".format(hostname))
            continue

        hosts_found.append(
            {
                "hostname": hostname,
                "host_id": host["id"],
            }
        )
        print(
            "{}: found Foreman host ID {}.".format(
                hostname,
                host["id"],
            )
        )

    if lookup_failed:
        print(
            "\nAt least one lookup failed. Aborting without deleting "
            "any hosts."
        )
        for host in hosts_found:
            report.append(
                make_summary_row(
                    item_type="Foreman Host",
                    name=host["hostname"],
                    target=host["host_id"],
                    status="Not Deleted",
                    details="Deletion aborted because a host lookup failed.",
                )
            )
        _write_report(report)
        return 1

    if not hosts_found:
        print("\nNo matching hosts were found.")
        _write_report(report)
        return 0

    confirmation = input(
        "\nType DELETE to permanently delete these {} Foreman host(s): "
        .format(len(hosts_found))
    ).strip()
    if confirmation != "DELETE":
        print("Cancelled; no hosts were deleted.")
        for host in hosts_found:
            report.append(
                make_summary_row(
                    item_type="Foreman Host",
                    name=host["hostname"],
                    target=host["host_id"],
                    status="Not Deleted",
                    details="Deletion was not confirmed.",
                )
            )
        _write_report(report)
        return 0

    for host in hosts_found:
        hostname = host["hostname"]
        host_id = host["host_id"]
        started_at = time.time()
        try:
            response = foreman.delete_host(host_id)
            response.raise_for_status()
            report.append(
                make_summary_row(
                    item_type="Foreman Host",
                    name=hostname,
                    target=host_id,
                    status="Successful",
                    time_seconds=time.time() - started_at,
                    details="Host deleted from Foreman (HTTP {}).".format(
                        response.status_code
                    ),
                )
            )
            print("{}: deleted.".format(hostname))
        except Exception as exc:
            report.append(
                make_summary_row(
                    item_type="Foreman Host",
                    name=hostname,
                    target=host_id,
                    status="Failed",
                    time_seconds=time.time() - started_at,
                    details="Deletion failed: {}".format(exc),
                )
            )
            print("{}: deletion failed: {}".format(hostname, exc))

    _write_report(report)
    return 1 if any(row["Status"] == "Failed" for row in report) else 0


def _write_report(report):
    print_summary_report(
        report,
        title="FINAL FOREMAN HOST DELETION SUMMARY",
    )
    write_summary_csv(
        report,
        vars.SCRIPT_ARTIFACT_PREFIXES["delete_foreman_hosts"],
    )


if __name__ == "__main__":
    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES[
                "delete_foreman_hosts"
            ],
            title="FOREMAN HOST DELETION",
        )
    )
