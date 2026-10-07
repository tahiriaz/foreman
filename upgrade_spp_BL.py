import concurrent.futures
import sys
import time

import pandas as pd
import requests

from configure_raid_BL import (
    ServerProcessor,
    load_resource_excel_fast,
    log,
)
from functions import vars
from functions.output_log import run_logged_main
from functions.reporting import (
    make_summary_row,
    print_summary_report,
    write_summary_csv,
)


EXCEL_PATH = vars.RESOURCE_LIST
SHEET_NAME = vars.SHEET_NAME
START_ROW = vars.START_ROW
END_ROW = vars.END_ROW
EXCEL_EMPTY_ROW_STOP = vars.RAID_EXCEL_EMPTY_ROW_STOP

ISO_URL = vars.SPP_BL_ISO_URL
VALID_EQUIPMENT_TYPES = list(vars.RAID_BL_EQUIPMENT_TYPES)
REQUIRED_COLUMNS = list(vars.RAID_BL_REQUIRED_COLUMNS)
MAX_WORKERS = vars.RAID_MAX_WORKERS
UPGRADE_WAIT_SECONDS = vars.SPP_BL_UPGRADE_WAIT_MINUTES * 60
POWER_OFF_VERIFY_TIMEOUT_SECONDS = (
    vars.SPP_BL_POWER_OFF_VERIFY_TIMEOUT_SECONDS
)
POWER_OFF_POLL_INTERVAL_SECONDS = (
    vars.SPP_BL_POWER_OFF_POLL_INTERVAL_SECONDS
)


def _request_checked(server, method, url, **kwargs):
    response = server._request(method, url, **kwargs)
    response.raise_for_status()
    return response


def _set_boot_override(server, target):
    system_url = "{}/redfish/v1/Systems/1/".format(server.base_url)
    _request_checked(
        server,
        "PATCH",
        system_url,
        json={
            "Boot": {
                "BootSourceOverrideTarget": target,
                "BootSourceOverrideEnabled": (
                    "Once" if target == "Cd" else "Disabled"
                ),
            }
        },
    )
    if target == "Cd":
        system_data = _request_checked(
            server,
            "GET",
            system_url,
        ).json()
        boot = system_data.get("Boot", {})
        if (
            boot.get("BootSourceOverrideTarget") != "Cd"
            or boot.get("BootSourceOverrideEnabled") != "Once"
        ):
            raise RuntimeError(
                "iLO did not confirm one-time CD/DVD boot."
            )


def _reboot_for_cdrom(server, power_state):
    reset_type = "ForceRestart" if power_state == "On" else "On"
    reset_url = (
        "{}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset".format(
            server.base_url
        )
    )
    _request_checked(
        server,
        "POST",
        reset_url,
        json={"ResetType": reset_type},
    )
    return reset_type


def _power_off_and_verify(server, slot, ip):
    power_state = server.get_system_info()
    if power_state != "Off":
        log(slot, ip, "60-minute wait ended; sending ForceOff through iLO.")
        reset_url = (
            "{}/redfish/v1/Systems/1/Actions/ComputerSystem.Reset".format(
                server.base_url
            )
        )
        _request_checked(
            server,
            "POST",
            reset_url,
            json={"ResetType": "ForceOff"},
        )
    else:
        log(slot, ip, "Blade is already powered off.")

    attempts = max(
        1,
        int(
            POWER_OFF_VERIFY_TIMEOUT_SECONDS
            / POWER_OFF_POLL_INTERVAL_SECONDS
        ),
    )
    last_error = None
    for attempt in range(attempts):
        if attempt:
            time.sleep(POWER_OFF_POLL_INTERVAL_SECONDS)
        try:
            if server.get_system_info() == "Off":
                log(slot, ip, "iLO confirms the blade is powered off.")
                return
            last_error = None
        except requests.exceptions.RequestException as exc:
            last_error = exc
            log(slot, ip, "Waiting for iLO to confirm power-off: {}".format(exc))

    if last_error is not None:
        raise RuntimeError(
            "Could not verify blade power-off after {} seconds: {}".format(
                POWER_OFF_VERIFY_TIMEOUT_SECONDS,
                last_error,
            )
        )
    raise RuntimeError(
        "Blade did not reach PowerState=Off within {} seconds.".format(
            POWER_OFF_VERIFY_TIMEOUT_SECONDS
        )
    )


def _wait_for_upgrade_window(slot, ip):
    deadline = time.monotonic() + UPGRADE_WAIT_SECONDS
    next_log = time.monotonic() + 300

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return

        time.sleep(min(remaining, max(1, next_log - time.monotonic())))
        if time.monotonic() >= next_log:
            elapsed = UPGRADE_WAIT_SECONDS - max(
                0,
                deadline - time.monotonic(),
            )
            log(
                slot,
                ip,
                "SPP boot window: {} of {} minutes elapsed.".format(
                    int(elapsed // 60),
                    vars.SPP_BL_UPGRADE_WAIT_MINUTES,
                ),
            )
            next_log += 300


def _eject_virtual_media(server, eject_uri):
    if not eject_uri:
        raise RuntimeError("iLO did not provide a virtual media eject action.")
    eject_url = (
        eject_uri
        if eject_uri.startswith("http")
        else "{}{}".format(server.base_url, eject_uri)
    )
    _request_checked(server, "POST", eject_url, json={})


def process_blade(server_data):
    ip = server_data["ilo_ip"]
    slot = server_data["enclosure_slot"]
    server = ServerProcessor(ip, slot, vars.ILO_BL_USERNAME, vars.ILO_BL_PASSWORD)
    started_at = time.time()
    eject_uri = None
    boot_override_set = False
    reboot_sent = False

    try:
        log(slot, ip, "Starting Gen9 SPP upgrade boot process...")
        server.authenticate()
        power_state = server.get_system_info()
        eject_uri = server.mount_virtual_media(ISO_URL)
        if not eject_uri:
            raise RuntimeError(
                "SPP ISO was mounted, but iLO did not provide an eject action."
            )

        _set_boot_override(server, "Cd")
        boot_override_set = True
        reset_type = _reboot_for_cdrom(server, power_state)
        reboot_sent = True
        log(
            slot,
            ip,
            "One-time CD/DVD boot configured; {} command sent.".format(
                reset_type
            ),
        )

        log(
            slot,
            ip,
            "Waiting {} minutes before powering off. "
            "Upgrade completion is not verified.".format(
                vars.SPP_BL_UPGRADE_WAIT_MINUTES
            ),
        )
        _wait_for_upgrade_window(slot, ip)

        _power_off_and_verify(server, slot, ip)
        _set_boot_override(server, "None")
        boot_override_set = False
        _eject_virtual_media(server, eject_uri)
        eject_uri = None

        status = "Successful"
        reason = (
            "SPP ISO booted; powered off after {} minutes; "
            "power-off verified; ISO ejected".format(
                vars.SPP_BL_UPGRADE_WAIT_MINUTES
            )
        )
    except Exception as exc:
        status = "Failed"
        reason = str(exc)

        if not reboot_sent:
            cleanup_errors = []
            if boot_override_set:
                try:
                    _set_boot_override(server, "None")
                except Exception as cleanup_exc:
                    cleanup_errors.append(
                        "boot override cleanup failed: {}".format(
                            cleanup_exc
                        )
                    )
            if eject_uri:
                try:
                    _eject_virtual_media(server, eject_uri)
                except Exception as cleanup_exc:
                    cleanup_errors.append(
                        "virtual media eject failed: {}".format(
                            cleanup_exc
                        )
                    )
            if cleanup_errors:
                reason += "; " + "; ".join(cleanup_errors)

        log(slot, ip, "FAILED: {}".format(reason))
    finally:
        server.session.close()

    return {
        "slot": slot,
        "ip": ip,
        "status": status,
        "reason": reason,
        "time_seconds": round(time.time() - started_at, 2),
    }


def main():
    try:
        print(
            "Loading data from {} (Sheet: '{}')...".format(
                EXCEL_PATH,
                SHEET_NAME,
            )
        )
        inventory = load_resource_excel_fast(
            EXCEL_PATH,
            SHEET_NAME,
            START_ROW,
            END_ROW,
            EXCEL_EMPTY_ROW_STOP,
        )
    except Exception as exc:
        print("Failed to read inventory: {}".format(exc))
        return 1

    target_enclosure = input(
        "\nEnter the Enclosure Name to process: "
    ).strip()
    if not target_enclosure:
        print("ERROR: Enclosure name cannot be empty.")
        return 1

    required_identifiers = {
        "enclosure_physical_name",
        "equipment_type",
    }
    if not required_identifiers.issubset(inventory.columns):
        print("ERROR: Inventory is missing required identifier columns.")
        return 1

    filtered = inventory[
        (inventory["enclosure_physical_name"] == target_enclosure)
        & inventory["equipment_type"].isin(VALID_EQUIPMENT_TYPES)
    ]
    if filtered.empty:
        print(
            "\nNo blade servers found for enclosure '{}'. Exiting.".format(
                target_enclosure
            )
        )
        return 0

    report = []
    servers_to_process = []
    for _, row in filtered.iterrows():
        raw_slot = row.get("enclosure_slot")
        raw_ip = row.get("ilo_ip")
        slot = (
            int(raw_slot)
            if pd.notna(raw_slot) and str(raw_slot).isdigit()
            else 999
        )
        ip = str(raw_ip).strip() if pd.notna(raw_ip) else "Unknown"
        missing = [
            column
            for column in REQUIRED_COLUMNS
            if column not in row
            or pd.isna(row[column])
            or str(row[column]).strip() == ""
        ]

        if missing:
            report.append(
                make_summary_row(
                    row="Slot {:02}".format(slot) if slot != 999 else "Slot ??",
                    item_type="Gen9 Blade Server",
                    name=target_enclosure,
                    target=ip,
                    status="Skipped",
                    details="Missing required values: {}".format(
                        ", ".join(missing)
                    ),
                )
            )
            log(slot, ip, "Skipping; missing required values: {}".format(missing))
            continue

        servers_to_process.append(
            {"enclosure_slot": slot, "ilo_ip": ip}
        )

    print(
        "\nValid Gen9 blade servers found: {}".format(
            len(servers_to_process)
        )
    )
    if not servers_to_process:
        print_summary_report(
            report,
            title="FINAL GEN9 SPP UPGRADE SUMMARY",
        )
        write_summary_csv(
            report,
            vars.SCRIPT_ARTIFACT_PREFIXES["upgrade_spp_BL"],
        )
        return 1

    print(
        "\nWARNING: Each selected blade will boot from the SPP ISO, "
        "then be forcibly powered off through iLO after {} minutes. "
        "The script cannot verify that the firmware upgrade has completed."
        .format(vars.SPP_BL_UPGRADE_WAIT_MINUTES)
    )
    confirmation = input(
        "Continue with enclosure '{}'? (yes/no): ".format(
            target_enclosure
        )
    ).strip().lower()
    if confirmation != "yes":
        print("Cancelled; no blades were changed.")
        return 0

    worker_count = min(MAX_WORKERS, len(servers_to_process))
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:
        futures = [
            executor.submit(process_blade, server_data)
            for server_data in servers_to_process
        ]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            row_label = (
                "Slot {:02}".format(result["slot"])
                if result["slot"] != 999
                else "Slot ??"
            )
            report.append(
                make_summary_row(
                    row=row_label,
                    item_type="Gen9 Blade Server",
                    name=target_enclosure,
                    target=result["ip"],
                    status=result["status"],
                    time_seconds=result["time_seconds"],
                    details=result["reason"],
                )
            )

    print_summary_report(
        report,
        title="FINAL GEN9 SPP UPGRADE SUMMARY",
    )
    write_summary_csv(
        report,
        vars.SCRIPT_ARTIFACT_PREFIXES["upgrade_spp_BL"],
    )
    return 1 if any(row["Status"] == "Failed" for row in report) else 0


if __name__ == "__main__":
    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES["upgrade_spp_BL"],
            title="GEN9 SPP BLADE UPGRADE",
        )
    )
