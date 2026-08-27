# BUILD_MARKER: DNS_SHARED_OPTIMIZED_V2_20260828

import csv
import os
import subprocess
import tempfile
import threading
import uuid

from functions import vars
from functions.shared import is_valid


_dns_print_lock = threading.Lock()
_dns_temp_dir_lock = threading.Lock()


def _print_dns(message, label=None):
    """Print one complete DNS log line immediately."""
    if label:
        output = "[DNS | {}] {}".format(
            label,
            message,
        )
    else:
        output = str(message)

    with _dns_print_lock:
        print(
            output,
            flush=True,
        )


def _clean(value):
    """Return a stripped string value."""
    return str(value).strip()


def _add_record(records, seen, hostname, record_type, target):
    """
    Add one valid DNS record while preventing duplicate operations.

    Duplicate comparison is case-insensitive for hostname/type/target.
    """
    if not is_valid(hostname) or not is_valid(target):
        return

    hostname = _clean(hostname)
    record_type = _clean(record_type).upper()
    target = _clean(target)

    key = (
        hostname.lower(),
        record_type,
        target.lower(),
    )

    if key in seen:
        return

    seen.add(key)
    records.append({
        "hostname": hostname,
        "RecordType": record_type,
        "Target": target,
    })


def build_dns_records(vm):
    """
    Build the DNS records required for one resource.

    This is shared by Foreman physical-host processing, VM processing and the
    standalone create_dns_records.py script.
    """
    records = []
    seen = set()

    logical_name = vm.get("logical_name")
    hostname = vm.get("hostname")

    # iLO A record.
    _add_record(
        records,
        seen,
        vm.get("ilo_hostname"),
        "A",
        vm.get("ilo_ip"),
    )

    fe_valid = is_valid(
        vm.get("fe_ip_address")
    )
    me_valid = is_valid(
        vm.get("me_ip_address")
    )

    # FE + ME:
    #   primary logical name -> ME IP
    #   FE logical name      -> FE IP
    if fe_valid and me_valid:
        _add_record(
            records,
            seen,
            logical_name,
            "A",
            vm.get("me_ip_address"),
        )

        _add_record(
            records,
            seen,
            vm.get("alias_domain"),
            "CNAME",
            logical_name,
        )

        _add_record(
            records,
            seen,
            vm.get("me_logical_naming"),
            "CNAME",
            logical_name,
        )

        _add_record(
            records,
            seen,
            vm.get("fe_logical_naming"),
            "A",
            vm.get("fe_ip_address"),
        )

    # FE only:
    #   primary logical name -> FE IP
    elif fe_valid:
        _add_record(
            records,
            seen,
            logical_name,
            "A",
            vm.get("fe_ip_address"),
        )

        _add_record(
            records,
            seen,
            vm.get("alias_domain"),
            "CNAME",
            logical_name,
        )

        _add_record(
            records,
            seen,
            vm.get("fe_logical_naming"),
            "CNAME",
            logical_name,
        )

    # BE A record.
    _add_record(
        records,
        seen,
        vm.get("be_logical_name"),
        "A",
        vm.get("be_ip_address"),
    )

    # CL A record.
    _add_record(
        records,
        seen,
        vm.get("cl_logical_name"),
        "A",
        vm.get("cl_ip_address"),
    )

    return records


def _get_temp_dir():
    """
    Return the shared DNS temporary directory.

    Directory creation is protected because multiple DNS workers may start at
    exactly the same time.
    """
    temp_dir = os.path.join(
        tempfile.gettempdir(),
        vars.DNS_TEMP_DIR_NAME,
    )

    if os.path.isdir(temp_dir):
        return temp_dir

    with _dns_temp_dir_lock:
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)

    return temp_dir


def run_dns_script(
    file_path,
    dns_server,
    domain,
    user,
    password,
    label=None,
):
    """
    Run the DNS PowerShell script and stream stdout/stderr live.

    stdout and stderr are deliberately merged so messages stay in execution
    order and no second pipe can block while several DNS jobs run in parallel.
    """
    script = vars.DNS_SCRIPT

    command = [
        vars.POWERSHELL_EXECUTABLE,
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        script,
        "-FileName",
        file_path,
        "-DnsServer",
        dns_server,
        "-DomainName",
        domain,
        "-Username",
        user,
        "-Password",
        password,
    ]

    output_lines = []
    process = None

    try:
        if not os.path.isfile(script):
            message = (
                "DNS PowerShell script not found: {}"
                .format(script)
            )

            _print_dns(
                message,
                label,
            )

            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": message,
            }

        _print_dns(
            "PowerShell DNS process starting...",
            label,
        )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )

        _print_dns(
            "PowerShell process launched (PID={}).".format(
                process.pid
            ),
            label,
        )

        while True:
            line = process.stdout.readline()

            if line:
                line = line.rstrip(
                    "\r\n"
                )

                output_lines.append(
                    line
                )

                _print_dns(
                    line,
                    label,
                )

                continue

            if process.poll() is not None:
                break

        remaining = process.stdout.read()

        if remaining:
            for line in remaining.splitlines():
                output_lines.append(
                    line
                )

                _print_dns(
                    line,
                    label,
                )

        returncode = process.wait()

        output = "\n".join(
            output_lines
        ).strip()

        if returncode == 0:
            _print_dns(
                "PowerShell DNS process completed successfully.",
                label,
            )
        else:
            _print_dns(
                "PowerShell DNS process FAILED with return code {}."
                .format(returncode),
                label,
            )

        return {
            "success": returncode == 0,
            "returncode": returncode,
            "stdout": output,
            # stderr is merged into stdout intentionally.
            "stderr": "",
        }

    except Exception as exc:
        if (
            process is not None
            and process.poll() is None
        ):
            try:
                process.kill()
            except Exception:
                pass

        message = (
            "Exception while executing DNS PowerShell script: {}"
            .format(exc)
        )

        _print_dns(
            message,
            label,
        )

        return {
            "success": False,
            "returncode": -1,
            "stdout": "\n".join(
                output_lines
            ).strip(),
            "stderr": message,
        }

    finally:
        if (
            process is not None
            and process.stdout is not None
        ):
            try:
                process.stdout.close()
            except Exception:
                pass


def create_dns_records(vm):
    """
    Generate and apply DNS records for one resource.

    Concurrency characteristics:
      - each worker owns a unique temporary CSV;
      - PowerShell output is streamed live;
      - console lines are thread-safe;
      - duplicate DNS operations inside one resource are removed;
      - there is no global DNS lock, so DNS for different hosts can run in
        parallel and can overlap Foreman creation for later hosts.
    """
    logical_name = str(
        vm.get(
            "logical_name",
            vm.get(
                "hostname",
                "Unknown",
            ),
        )
    ).strip()

    records = build_dns_records(
        vm
    )

    if not records:
        _print_dns(
            "No valid DNS records generated.",
            logical_name,
        )

        return {
            "status": "Skipped",
            "records": 0,
            "returncode": "",
            "details": "No valid DNS records generated",
        }

    temp_dir = _get_temp_dir()

    safe_logical_name = (
        logical_name
        .replace("\\", "_")
        .replace("/", "_")
        .replace(":", "_")
    )

    unique_name = (
        "dns_{}_{}.csv".format(
            safe_logical_name,
            uuid.uuid4().hex,
        )
    )

    csv_path = os.path.join(
        temp_dir,
        unique_name,
    )

    try:
        with open(
            csv_path,
            "w",
            newline="",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=[
                    "hostname",
                    "RecordType",
                    "Target",
                ],
            )

            writer.writeheader()
            writer.writerows(
                records
            )

        _print_dns(
            "STARTING - {} DNS record(s) generated."
            .format(
                len(records)
            ),
            logical_name,
        )

        _print_dns(
            "Temporary DNS CSV: {}".format(
                csv_path
            ),
            logical_name,
        )

        result = run_dns_script(
            csv_path,
            vars.DNS_SERVER,
            vars.DOMAIN_NAME,
            vars.DNS_SERVER_USER,
            vars.DNS_SERVER_PASS,
            label=logical_name,
        )

        if not result["success"]:
            details = (
                result["stderr"]
                or result["stdout"]
                or "PowerShell DNS operation failed"
            )

            _print_dns(
                "FAILED - {}".format(
                    details
                ),
                logical_name,
            )

            return {
                "status": "Failed",
                "records": len(records),
                "returncode": result[
                    "returncode"
                ],
                "details": details,
            }

        _print_dns(
            "COMPLETED SUCCESSFULLY.",
            logical_name,
        )

        return {
            "status": "Successful",
            "records": len(records),
            "returncode": result[
                "returncode"
            ],
            "details": (
                "DNS records created successfully"
            ),
        }

    except Exception as exc:
        message = (
            "DNS processing exception: {}"
            .format(exc)
        )

        _print_dns(
            message,
            logical_name,
        )

        return {
            "status": "Failed",
            "records": len(records),
            "returncode": -1,
            "details": message,
        }

    finally:
        try:
            if os.path.exists(csv_path):
                os.remove(csv_path)

                _print_dns(
                    "Temporary DNS CSV removed.",
                    logical_name,
                )

        except Exception as exc:
            _print_dns(
                "WARNING: Could not remove temporary DNS CSV: {}"
                .format(exc),
                logical_name,
            )
