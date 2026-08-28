import concurrent.futures
import time

from functions import dns, vars
from functions.inventory import load_inventory, validate_resource


def provision_from_excel(
    file_path=None,
    sheet=None,
    start_row=None,
    end_row=None,
    max_workers=None,
):
    from functions import process_host, process_vm

    file_path = vars.RESOURCE_LIST if file_path is None else file_path
    sheet = vars.SHEET_NAME if sheet is None else sheet
    start_row = vars.START_ROW if start_row is None else start_row
    end_row = vars.END_ROW if end_row is None else end_row
    max_workers = vars.MAX_WORKERS if max_workers is None else max_workers

    max_workers = max(1, int(max_workers))

    processor_map = {
        "ESXi": dns.create_dns_records,
        "NVR": process_host.create,
        "NVR Blade Server": process_host.create,
        "VCA": process_host.create,
        "VCA Blade Server": process_host.create,
        "Virtual Machine": process_vm.create,
        "Virtual IP": dns.create_dns_records,
        "Enclosure OA": dns.create_dns_records,
        "Enclosure Switch": dns.create_dns_records,
        "Server Enclosure": dns.create_dns_records,
    }

    vm_list = load_inventory(file_path, sheet, start_row, end_row)
    if not vm_list:
        print("No rows found in requested Excel range.")
        return []

    jobs = []
    results = []

    for excel_row, vm in enumerate(vm_list, start=start_row):
        validation = validate_resource(vm, excel_row)
        eq_type = validation["equipment_type"]
        logical_name = validation["logical_name"]

        if not validation["valid"]:
            print(
                f"WARNING (Row {excel_row}): {validation['details']} "
                f"Skipping."
            )
            results.append({
                "ExcelRow": excel_row,
                "EquipmentType": eq_type,
                "LogicalName": logical_name,
                "Status": validation["status"],
                "Foreman": "N/A",
                "DNS": "N/A",
                "Ansible": "N/A",
                "Details": validation["details"],
                "TimeSeconds": 0.0,
            })
            continue

        process_func = processor_map.get(eq_type)
        if not process_func:
            details = (
                f"No processing function mapped for equipment_type '{eq_type}'."
            )
            results.append({
                "ExcelRow": excel_row,
                "EquipmentType": eq_type,
                "LogicalName": logical_name,
                "Status": "Skipped",
                "Foreman": "N/A",
                "DNS": "N/A",
                "Ansible": "N/A",
                "Details": details,
                "TimeSeconds": 0.0,
            })
            continue

        jobs.append({
            "excel_row": excel_row,
            "equipment_type": eq_type,
            "logical_name": logical_name,
            "vm": vm,
            "process_func": process_func,
        })

    if not jobs:
        print("\nNo valid resources left to process.")
        return results

    worker_count = min(max_workers, len(jobs))
    print(f"\nValid resources to process: {len(jobs)}")
    print(f"Parallel workers: {worker_count}\n")

    def execute_job(job):
        excel_row = job["excel_row"]
        eq_type = job["equipment_type"]
        logical_name = job["logical_name"]
        vm = job["vm"]
        process_func = job["process_func"]

        start_time = time.time()
        print(
            f"[Row {excel_row} | {logical_name} | {eq_type}] STARTING",
            flush=True,
        )

        try:
            function_result = process_func(vm)

            if isinstance(function_result, dict):
                status = function_result.get("status")
                details = function_result.get(
                    "details",
                    function_result.get("message", ""),
                )

                if not status:
                    if "success" in function_result:
                        status = (
                            "Successful"
                            if function_result["success"]
                            else "Failed"
                        )
                    else:
                        status = "Successful"

                foreman_status = function_result.get(
                    "foreman_status", "N/A"
                )
                dns_status = function_result.get("dns_status", "N/A")
                ansible_status = function_result.get(
                    "ansible_status", "N/A"
                )

                if process_func is dns.create_dns_records:
                    dns_status = status
            elif function_result is False:
                status = "Failed"
                details = "Processor returned False"
                foreman_status = dns_status = ansible_status = "N/A"
            elif function_result is True:
                status = "Successful"
                details = "Processor completed successfully"
                foreman_status = dns_status = ansible_status = "N/A"
            else:
                status = "Successful"
                details = "Processor completed"
                foreman_status = dns_status = ansible_status = "N/A"
        except Exception as exc:
            status = "Failed"
            details = str(exc)
            foreman_status = dns_status = ansible_status = "Unknown"

        elapsed = time.time() - start_time
        print(
            f"[Row {excel_row} | {logical_name} | {eq_type}] "
            f"FINISHED - {status}",
            flush=True,
        )

        return {
            "ExcelRow": excel_row,
            "EquipmentType": eq_type,
            "LogicalName": logical_name,
            "Status": status,
            "Foreman": foreman_status,
            "DNS": dns_status,
            "Ansible": ansible_status,
            "Details": details,
            "TimeSeconds": round(elapsed, 2),
        }

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:
        future_map = {
            executor.submit(execute_job, job): job for job in jobs
        }

        for future in concurrent.futures.as_completed(future_map):
            job = future_map[future]
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({
                    "ExcelRow": job["excel_row"],
                    "EquipmentType": job["equipment_type"],
                    "LogicalName": job["logical_name"],
                    "Status": "Failed",
                    "Foreman": "Unknown",
                    "DNS": "Unknown",
                    "Ansible": "Unknown",
                    "Details": f"Unhandled worker exception: {exc}",
                    "TimeSeconds": 0.0,
                })

    return results
