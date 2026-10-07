import concurrent.futures
import sys
import time

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from functions import vars
from functions.inventory import load_inventory
from functions.output_log import run_logged_main
from functions.reporting import (
    make_summary_row,
    print_summary_report,
    write_summary_csv,
)
from functions.shared import is_valid


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = vars.ILO_BL_USERNAME
PASSWORD = vars.ILO_BL_PASSWORD
REQUEST_TIMEOUT_SECONDS = vars.RAID_BL_REQUEST_TIMEOUT_SECONDS


def log(slot, ip, message):
    try:
        slot_text = "{:02}".format(int(slot))
    except (TypeError, ValueError):
        slot_text = "??"
    print("[Slot {} | {}] {}".format(slot_text, ip, message))


class BladeIlo:
    def __init__(self, ip, slot):
        self.ip = ip
        self.slot = slot
        self.base_url = "https://{}".format(ip)
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({"Content-Type": "application/json"})

        retries = Retry(
            total=vars.RAID_HTTP_RETRY_TOTAL,
            backoff_factor=vars.RAID_HTTP_RETRY_BACKOFF_FACTOR,
            status_forcelist=list(vars.RAID_HTTP_RETRY_STATUS_CODES),
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", REQUEST_TIMEOUT_SECONDS)
        return self.session.request(method, url, **kwargs)

    def authenticate(self):
        url = "{}/redfish/v1/SessionService/Sessions".format(
            self.base_url
        )
        response = self.request(
            "POST",
            url,
            json={"UserName": USERNAME, "Password": PASSWORD},
        )
        response.raise_for_status()

        token = response.headers.get("X-Auth-Token")
        if not token:
            raise RuntimeError("iLO authentication response did not include a session token.")

        self.session.headers.update({"X-Auth-Token": token})

    def set_pxe_once_and_reboot(self):
        system_url = "{}/redfish/v1/Systems/1/".format(self.base_url)
        response = self.request("GET", system_url)
        response.raise_for_status()
        power_state = response.json().get("PowerState", "Unknown")

        response = self.request(
            "PATCH",
            system_url,
            json={
                "Boot": {
                    "BootSourceOverrideTarget": "Pxe",
                    "BootSourceOverrideEnabled": "Once",
                }
            },
        )
        response.raise_for_status()

        response = self.request("GET", system_url)
        response.raise_for_status()
        boot = response.json().get("Boot", {})
        if (
            boot.get("BootSourceOverrideTarget") != "Pxe"
            or boot.get("BootSourceOverrideEnabled") != "Once"
        ):
            raise RuntimeError(
                "iLO did not confirm the one-time PXE boot setting."
            )

        reset_type = "ForceRestart" if power_state == "On" else "On"
        reset_url = (
            "{}Actions/ComputerSystem.Reset".format(system_url)
        )
        response = self.request(
            "POST",
            reset_url,
            json={"ResetType": reset_type},
        )
        response.raise_for_status()
        return reset_type


def process_blade(server_data):
    ip = server_data["ilo_ip"]
    slot = server_data["enclosure_slot"]
    server = BladeIlo(ip, slot)
    started_at = time.time()

    try:
        log(slot, ip, "Authenticating to iLO...")
        server.authenticate()
        reset_type = server.set_pxe_once_and_reboot()
        log(
            slot,
            ip,
            "One-time network/PXE boot configured; {} command sent.".format(
                reset_type
            ),
        )
        return {
            "slot": slot,
            "ip": ip,
            "status": "Successful",
            "reason": "One-time PXE boot set; {} command sent".format(
                reset_type
            ),
            "time_seconds": round(time.time() - started_at, 2),
        }
    except Exception as exc:
        log(slot, ip, "FAILED: {}".format(exc))
        return {
            "slot": slot,
            "ip": ip,
            "status": "Failed",
            "reason": str(exc),
            "time_seconds": round(time.time() - started_at, 2),
        }
    finally:
        server.session.close()


def main():
    try:
        inventory = load_inventory()
    except Exception as exc:
        print("Failed to read inventory: {}".format(exc))
        return 1

    if not inventory:
        print("Inventory contains no records in the configured Excel row range.")
        return 0

    target_enclosure = input(
        "\nEnter the Enclosure Name to process: "
    ).strip()
    if not target_enclosure:
        print("ERROR: Enclosure name cannot be empty.")
        return 1

    required_columns = {
        "enclosure_physical_name",
        "equipment_type",
        "enclosure_slot",
        "ilo_ip",
    }
    if not required_columns.issubset(inventory[0]):
        print("ERROR: Inventory is missing required blade identifier columns.")
        return 1

    enclosure_rows = [
        row
        for row in inventory
        if str(row.get("enclosure_physical_name", "")).strip()
        == target_enclosure
        and row.get("equipment_type") in vars.ILO_BL_VALID_EQUIPMENT_TYPES
    ]
    if not enclosure_rows:
        print(
            "\nNo blade servers found for enclosure '{}'. Exiting.".format(
                target_enclosure
            )
        )
        return 0

    report = []
    servers_to_process = []
    for row in enclosure_rows:
        slot = row.get("enclosure_slot", "??")
        ip = str(row.get("ilo_ip", "")).strip()
        missing = [
            column
            for column in ("enclosure_slot", "ilo_ip")
            if not is_valid(row.get(column))
        ]

        if missing:
            report.append(
                make_summary_row(
                    row="Slot {}".format(slot),
                    item_type="Blade Server",
                    name=target_enclosure,
                    target=ip or "Unknown",
                    status="Skipped",
                    details="Missing required values: {}".format(
                        ", ".join(missing)
                    ),
                )
            )
            continue

        try:
            slot = int(slot)
        except (TypeError, ValueError):
            slot = str(slot)

        servers_to_process.append(
            {"enclosure_slot": slot, "ilo_ip": ip}
        )

    print(
        "\nBlade servers found for enclosure '{}': {}".format(
            target_enclosure,
            len(enclosure_rows),
        )
    )
    print("Valid iLO targets to reboot: {}".format(len(servers_to_process)))
    if not servers_to_process:
        print("No valid iLO targets to process.")
        print_summary_report(
            report,
            title="FINAL BLADE PXE REBOOT SUMMARY",
        )
        write_summary_csv(
            report,
            vars.SCRIPT_ARTIFACT_PREFIXES["reboot_blades_BL"],
        )
        return 1

    confirmation = input(
        "\nSet one-time network/PXE boot and reboot every valid blade "
        "in this enclosure? (yes/no): "
    ).strip().lower()
    if confirmation != "yes":
        print("Cancelled; no blades were changed.")
        return 0

    print(
        "\nStarting one-time PXE configuration and iLO reboot for "
        "enclosure '{}'...".format(target_enclosure)
    )
    max_workers = min(
        vars.ILO_BL_REDFISH_CONCURRENT_SESSIONS,
        len(servers_to_process),
    )
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:
        futures = [
            executor.submit(process_blade, server)
            for server in servers_to_process
        ]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            report.append(
                make_summary_row(
                    row="Slot {}".format(result["slot"]),
                    item_type="Blade Server",
                    name=target_enclosure,
                    target=result["ip"],
                    status=result["status"],
                    time_seconds=result["time_seconds"],
                    details=result["reason"],
                )
            )

    print_summary_report(
        report,
        title="FINAL BLADE PXE REBOOT SUMMARY",
    )
    write_summary_csv(
        report,
        vars.SCRIPT_ARTIFACT_PREFIXES["reboot_blades_BL"],
    )

    return 1 if any(row["Status"] == "Failed" for row in report) else 0


if __name__ == "__main__":
    sys.exit(
        run_logged_main(
            main,
            log_prefix=vars.SCRIPT_ARTIFACT_PREFIXES[
                "reboot_blades_BL"
            ],
            title="BLADE NETWORK REBOOT",
        )
    )
