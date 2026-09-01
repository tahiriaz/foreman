# BUILD_MARKER: FOREMAN_VM_AFFINITY_V1_20260901

import time
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import requests

from functions import dns, foreman, vars, vmware_affinity
from functions.shared import is_valid


def get_compute_id():
    return foreman.get_cached_resource_id(
        "api/v2/compute_resources",
        vars.COMPUTE_RESOURCE,
    )


def get_image_id(image_name):
    compute_id = get_compute_id()
    return foreman.get_cached_resource_id(
        "api/v2/compute_resources/{}/images".format(compute_id),
        image_name,
    )


def get_ansible_job_id():
    return foreman.get_cached_resource_id(
        "api/v2/job_templates",
        vars.ANSIBLE_JOB_NAME,
    )


def sched_ansible_role(hostname, delay):
    """Schedule the configured Foreman Ansible job."""
    result = {
        "success": False,
        "hostname": hostname,
        "scheduled_time": None,
        "message": "",
    }

    try:
        start_time = (
            datetime.now(timezone.utc) + timedelta(seconds=int(delay))
        ).isoformat().replace("+00:00", "Z")
        result["scheduled_time"] = start_time

        payload = {
            "job_invocation": {
                "job_template_id": get_ansible_job_id(),
                "target_hosts": hostname,
                "targeting_type": vars.ANSIBLE_TARGETING_TYPE,
                "search_query": "name = {}".format(hostname),
                "scheduling": {"start_at": start_time},
                "description": (
                    "Scheduled Ansible run for {} after provisioning".format(
                        hostname
                    )
                ),
                "concurrency_control": {
                    "concurrency_level": vars.ANSIBLE_CONCURRENCY_LEVEL
                },
            }
        }

        response = foreman.post_job_invocation(payload)
        if response.status_code == 201:
            message = (
                "Ansible job for {} successfully scheduled to run at {}".format(
                    hostname,
                    start_time,
                )
            )
            print(message)
            result.update({"success": True, "message": message})
            return result

        result["message"] = (
            "Failed to schedule Ansible run job for {}. HTTP {}: {}".format(
                hostname,
                response.status_code,
                response.text,
            )
        )
    except requests.exceptions.Timeout as error:
        result["message"] = (
            "Timeout while scheduling Ansible job for {}: {}".format(
                hostname,
                error,
            )
        )
    except requests.exceptions.RequestException as error:
        result["message"] = (
            "HTTP/connection error while scheduling Ansible job for {}: {}"
            .format(hostname, error)
        )
    except Exception as error:
        result["message"] = (
            "Error scheduling Ansible run job for {}: {}".format(
                hostname,
                error,
            )
        )

    print(result["message"])
    return result


def _get_affinity_group(vm):
    """Return a normalized optional affinity group or an empty string."""
    value = vm.get(vars.VM_AFFINITY_GROUP_COLUMN)
    return str(value).strip() if is_valid(value) else ""


def _power_state_from_response(response):
    """Extract a normalized Foreman power state from an HTTP response."""
    try:
        data = response.json()
    except Exception:
        return ""

    if not isinstance(data, dict):
        return ""

    value = data.get("power", data.get("state", ""))
    if isinstance(value, bool):
        return "on" if value else "off"

    return str(value or "").strip().lower().replace("_", "")


def _is_powered_on_state(state):
    return state in ("on", "running", "poweredon", "true", "1")


def _power_on_vm_via_foreman(hostname):
    """Start a Foreman-managed VM and verify that it reaches power state On."""
    result = {
        "success": False,
        "status": "Failed",
        "message": "",
    }
    host_id = quote(str(hostname).strip(), safe="")
    url = "{}/api/v2/hosts/{}/power".format(
        vars.FOREMAN_URL.rstrip("/"),
        host_id,
    )
    timeout = (
        vars.HTTP_CONNECT_TIMEOUT,
        vars.HTTP_READ_TIMEOUT,
    )
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.put(
            url,
            auth=(vars.USER, vars.PASSWORD),
            headers=headers,
            json={"power_action": "start"},
            verify=vars.VERIFY_SSL,
            timeout=timeout,
        )

        if response.status_code not in (200, 201, 202):
            result["message"] = (
                "Foreman failed to start VM '{}'. HTTP {}: {}".format(
                    hostname,
                    response.status_code,
                    response.text,
                )
            )
            return result

        state = _power_state_from_response(response)
        if _is_powered_on_state(state):
            result.update({
                "success": True,
                "status": "Successful",
                "message": "VM '{}' powered on successfully".format(hostname),
            })
            return result

        last_message = ""
        for attempt in range(1, vars.VM_AFFINITY_POWER_VERIFY_ATTEMPTS + 1):
            try:
                status_response = requests.get(
                    url,
                    auth=(vars.USER, vars.PASSWORD),
                    headers={"Accept": "application/json"},
                    params={
                        "timeout": str(
                            vars.VM_AFFINITY_POWER_STATUS_TIMEOUT_SECONDS
                        )
                    },
                    verify=vars.VERIFY_SSL,
                    timeout=timeout,
                )

                if status_response.status_code == 200:
                    state = _power_state_from_response(status_response)
                    if _is_powered_on_state(state):
                        result.update({
                            "success": True,
                            "status": "Successful",
                            "message": (
                                "VM '{}' powered on successfully; verified "
                                "after attempt {}/{}".format(
                                    hostname,
                                    attempt,
                                    vars.VM_AFFINITY_POWER_VERIFY_ATTEMPTS,
                                )
                            ),
                        })
                        return result

                    last_message = "reported power state '{}'".format(
                        state or "unknown"
                    )
                else:
                    last_message = "status HTTP {}: {}".format(
                        status_response.status_code,
                        status_response.text,
                    )
            except Exception as error:
                last_message = "power-status check failed: {}".format(error)

            if attempt < vars.VM_AFFINITY_POWER_VERIFY_ATTEMPTS:
                time.sleep(vars.VM_AFFINITY_POWER_VERIFY_DELAY_SECONDS)

        result["message"] = (
            "Foreman accepted the start request for VM '{}', but power-on "
            "could not be verified after {} attempts ({})".format(
                hostname,
                vars.VM_AFFINITY_POWER_VERIFY_ATTEMPTS,
                last_message or "no power state returned",
            )
        )
        return result

    except requests.exceptions.Timeout as error:
        result["message"] = (
            "Timeout while starting VM '{}' through Foreman: {}".format(
                hostname,
                error,
            )
        )
    except requests.exceptions.RequestException as error:
        result["message"] = (
            "HTTP/connection error while starting VM '{}' through Foreman: {}"
            .format(hostname, error)
        )
    except Exception as error:
        result["message"] = (
            "Error while starting VM '{}' through Foreman: {}".format(
                hostname,
                error,
            )
        )

    return result


def create(vm):
    """Create/reuse a VM, process optional affinity, DNS and Ansible."""
    hostname = str(vm.get("logical_name", "UNKNOWN")).strip()
    short_name = hostname.split(".", 1)[0]
    affinity_group = _get_affinity_group(vm)
    affinity_required = bool(affinity_group)

    result = {
        "success": False,
        "status": "Failed",
        "details": "",
        "hostname": hostname,
        "foreman_success": False,
        "foreman_status": "Failed",
        "foreman_message": "",
        "affinity_required": affinity_required,
        "affinity_success": not affinity_required,
        "affinity_status": "Pending" if affinity_required else "Not Required",
        "affinity_message": "",
        "power_required": affinity_required,
        "power_success": not affinity_required,
        "power_status": "Pending" if affinity_required else "Foreman Auto",
        "power_message": "",
        "dns_success": False,
        "dns_status": "Not Run",
        "dns_message": "",
        "ansible_success": False,
        "ansible_status": "Not Run",
        "ansible_message": "",
        "message": "",
    }

    try:
        existing = foreman.get_host(hostname, short_name)
        already_exists = bool(existing)

        if already_exists:
            _set_existing_vm(result, hostname, existing)
        else:
            payload = create_payload(vm)

            with foreman.host_creation_slot(hostname):
                # Final existence check under the same creation lock.
                existing = foreman.get_host(hostname, short_name)

                if existing:
                    already_exists = True
                    _set_existing_vm(result, hostname, existing)
                else:
                    response = foreman.create_host(payload)

                    if response.status_code == 201:
                        try:
                            created = foreman.verify_created_managed_host(
                                response=response,
                                expected_names=(hostname, short_name),
                                expected_organization_id=(
                                    payload["host"].get("organization_id")
                                ),
                                expected_location_id=(
                                    payload["host"].get("location_id")
                                ),
                            )
                        except Exception as verify_error:
                            host_id = foreman.get_response_host_id(response)
                            message = (
                                "CRITICAL: Foreman returned HTTP 201 for VM {}, "
                                "but POST-CREATE VERIFICATION FAILED. Foreman "
                                "host ID: {}. Error: {}. DNS, affinity and "
                                "Ansible will NOT run. Check Foreman before "
                                "rerunning this VM because manual cleanup may "
                                "be required.".format(
                                    hostname,
                                    host_id if host_id else "Unknown",
                                    verify_error,
                                )
                            )
                            print(message)
                            result.update({
                                "foreman_success": False,
                                "foreman_status": "Failed",
                                "foreman_message": message,
                                "message": message,
                                "details": message,
                            })
                            return result

                        foreman_message = foreman.describe_host(created)
                        result.update({
                            "foreman_success": True,
                            "foreman_status": "Successful",
                            "foreman_message": foreman_message,
                        })
                        print(
                            "Successfully created {} in Foreman.".format(
                                hostname
                            )
                        )
                        print(
                            "POST-CREATE VERIFICATION PASSED: {}".format(
                                foreman_message
                            )
                        )

                    elif foreman.is_duplicate_host_response(response):
                        existing = foreman.get_host(hostname, short_name)

                        if existing:
                            already_exists = True
                            _set_existing_vm(
                                result,
                                hostname,
                                existing,
                                duplicate_response=True,
                            )
                        else:
                            message = (
                                "Foreman returned duplicate-name HTTP 422 for "
                                "VM {}, but an exact managed-host lookup found "
                                "no matching host. Treating this as FAILED. "
                                "This can indicate a hidden/orphan Host::Base "
                                "record. Response: {}".format(
                                    hostname,
                                    response.text,
                                )
                            )
                            print(message)
                            result.update({
                                "message": message,
                                "details": message,
                            })
                            return result
                    else:
                        message = (
                            "Failed to create {}. HTTP {}: {}".format(
                                hostname,
                                response.status_code,
                                response.text,
                            )
                        )
                        print(message)
                        result.update({
                            "message": message,
                            "details": message,
                        })
                        return result

        # Foreman creation lock has been released here.
        if already_exists:
            result.update({
                "power_required": False,
                "power_success": True,
                "power_status": "Skipped",
                "power_message": "VM already exists; power state not changed",
            })

            if affinity_required:
                result.update({
                    "affinity_success": True,
                    "affinity_status": "Skipped",
                    "affinity_message": (
                        "VM already exists; affinity-group membership was "
                        "not modified"
                    ),
                })
        elif affinity_required:
            print(
                "VM {} requests affinity group '{}'. Foreman created the VM "
                "powered off; applying vSphere group membership before "
                "power-on.".format(hostname, affinity_group)
            )

            affinity_result = vmware_affinity.assign_vm_to_group(
                hostname,
                affinity_group,
            )
            result.update({
                "affinity_success": affinity_result["success"],
                "affinity_status": affinity_result["status"],
                "affinity_message": affinity_result["message"],
            })

            if affinity_result["success"]:
                print(affinity_result["message"])
            else:
                print(
                    "WARNING: {}. VM will still be started.".format(
                        affinity_result["message"]
                    )
                )

            power_result = _power_on_vm_via_foreman(hostname)
            result.update({
                "power_success": power_result["success"],
                "power_status": power_result["status"],
                "power_message": power_result["message"],
            })

            if power_result["success"]:
                print(power_result["message"])
            else:
                print("ERROR: {}".format(power_result["message"]))

        _process_dns(vm, result)

        if already_exists:
            result.update({
                "ansible_success": True,
                "ansible_status": "Skipped",
                "ansible_message": (
                    "VM already exists in Foreman; Ansible not rescheduled"
                ),
            })
            print(
                "Skipping Ansible scheduling for existing VM {}.".format(
                    hostname
                )
            )
        elif affinity_required and not result["power_success"]:
            result.update({
                "ansible_success": False,
                "ansible_status": "Not Run",
                "ansible_message": (
                    "Ansible was not scheduled because VM power-on failed"
                ),
            })
            print(
                "Skipping Ansible scheduling for {} because the VM could not "
                "be verified as powered on.".format(hostname)
            )
        else:
            ansible_result = sched_ansible_role(
                hostname,
                vars.ANSIBLE_DELAY,
            )
            result.update({
                "ansible_success": ansible_result["success"],
                "ansible_status": (
                    "Successful" if ansible_result["success"] else "Failed"
                ),
                "ansible_message": ansible_result["message"],
            })

        _finalize_result(result)
        return result

    except Exception as error:
        message = "Error processing Foreman VM {}: {}".format(
            hostname,
            error,
        )
        print(message)
        result.update({
            "message": message,
            "details": message,
        })
        return result


def _set_existing_vm(result, hostname, existing, duplicate_response=False):
    """Mark an exact managed VM host as already existing."""
    foreman_message = foreman.describe_host(existing)
    result.update({
        "foreman_success": True,
        "foreman_status": "Already Exists",
        "foreman_message": foreman_message,
    })

    if duplicate_response:
        print(
            "Foreman returned duplicate-name HTTP 422 for {}, and exact VM "
            "verification succeeded: {}".format(
                hostname,
                foreman_message,
            )
        )
    else:
        print(
            "Foreman VM {} already exists: {}".format(
                hostname,
                foreman_message,
            )
        )


def _process_dns(vm, result):
    """Run DNS processing and update the VM result."""
    hostname = result["hostname"]

    try:
        dns_result = dns.create_dns_records(vm)
        dns_success = dns_result.get("status") == "Successful"
        dns_message = dns_result.get("details", "")

        result.update({
            "dns_success": dns_success,
            "dns_status": dns_result.get("status", "Failed"),
            "dns_message": dns_message,
        })

        if dns_success:
            suffix = ": {}".format(dns_message) if dns_message else ""
            print("DNS creation completed for {}{}".format(hostname, suffix))
        else:
            print(
                "WARNING: Foreman stage completed for {}, but DNS failed: {}"
                .format(
                    hostname,
                    dns_message or "Unknown DNS error",
                )
            )
    except Exception as error:
        result.update({
            "dns_success": False,
            "dns_status": "Failed",
            "dns_message": str(error),
        })
        print(
            "WARNING: Foreman stage completed for {}, but DNS raised an "
            "exception: {}".format(hostname, error)
        )


def _component_text(status, message):
    return "{} ({})".format(status, message) if message else status


def _finalize_result(result):
    """Set overall VM provisioning status, including affinity warnings."""
    parts = [
        "Foreman: {}".format(
            _component_text(
                result["foreman_status"],
                result["foreman_message"],
            )
        ),
        "Affinity: {}".format(
            _component_text(
                result["affinity_status"],
                result["affinity_message"],
            )
        ),
        "Power: {}".format(
            _component_text(
                result["power_status"],
                result["power_message"],
            )
        ),
        "DNS: {}".format(
            _component_text(
                result["dns_status"],
                result["dns_message"],
            )
        ),
        "Ansible: {}".format(
            _component_text(
                result["ansible_status"],
                result["ansible_message"],
            )
        ),
    ]

    power_ok = (
        not result.get("power_required", False)
        or result.get("power_success", False)
    )
    affinity_warning = (
        result.get("affinity_required", False)
        and result.get("affinity_status") == "Warning"
    )

    components_ok = all((
        result["foreman_success"],
        power_ok,
        result["dns_success"],
        result["ansible_success"],
    ))
    result["success"] = components_ok and not affinity_warning
    result["status"] = "Successful" if result["success"] else "Partial"

    details = "; ".join(parts)
    result.update({
        "message": details,
        "details": details,
    })


def create_payload(vm):
    """Build a Foreman VM payload."""
    hostname = vm.get("logical_name", "UNKNOWN")

    if not is_valid(vm.get("logical_name")):
        raise ValueError("Missing logical_name for VM")

    hostgroup_name = foreman.gethostgroup(
        vm["subsystems"],
        vm["function"],
        vm["variation"],
    )

    if not is_valid(hostgroup_name):
        raise ValueError(
            "No Foreman hostgroup mapping found for {} / {} / {}".format(
                vm["subsystems"],
                vm["function"],
                vm["variation"],
            )
        )

    organization_id, location_id = foreman.get_scope_ids()
    affinity_group = _get_affinity_group(vm)
    start_on_create = "0" if affinity_group else vars.VM_START_ON_CREATE
    image_name = str(vm[vars.VM_IMAGE_NAME_COLUMN]).strip()

    payload = {
        "host": {
            "name": vm["logical_name"],
            "hostgroup_id": foreman.get_cached_resource_id(
                "api/v2/hostgroups",
                hostgroup_name,
            ),
            "organization_id": organization_id,
            "location_id": location_id,
            "compute_resource_id": get_compute_id(),
            "image_id": get_image_id(image_name),
            "provision_method": vars.VM_PROVISION_METHOD,
            "managed": True,
            "path": vm[vars.VM_FOLDER_COLUMN],
            "compute_attributes": {
                "cpus": int(vm["cpu"]),
                "memory_gb": int(vm["ram_(gb)"]),
                "start": start_on_create,
                "volumes_attributes": [],
            },
            "interfaces_attributes": [],
            "host_parameters_attributes": foreman.gethost_parameters(
                vm["foreman_parameters"],
                vm.get("ntp1", vars.EMPTY_VALUE),
                vm.get("ntp2", vars.EMPTY_VALUE),
            ),
        }
    }

    _add_interfaces(payload, vm)
    _add_disks(payload, vm)

    if not payload["host"]["compute_attributes"]["volumes_attributes"]:
        raise ValueError(
            "VM {} has no valid disks configured".format(hostname)
        )

    return payload


def _add_interfaces(payload, vm):
    """Add VM network interfaces."""
    hostname = vm.get("logical_name", "UNKNOWN")
    has_fe = is_valid(vm.get("fe_ip_address"))
    has_me = is_valid(vm.get("me_ip_address"))

    if not has_fe:
        if has_me:
            raise ValueError(
                "VM {} has a MiddleEnd IP address ({}) but no FrontEnd IP "
                "address. MiddleEnd-only provisioning is not defined.".format(
                    hostname,
                    vm.get("me_ip_address"),
                )
            )

        raise ValueError(
            "VM {} has no valid FrontEnd or MiddleEnd IP address".format(
                hostname
            )
        )

    domain_id = foreman.get_cached_resource_id(
        "api/domains",
        vm["domain_name"],
    )
    fe_subnet_id = foreman.get_cached_resource_id(
        "api/v2/subnets",
        vm["fe_vlan_name"],
    )
    base_name = str(vm["logical_name"]).replace(
        ".{}".format(vm["domain_name"]),
        "",
    )

    if has_me:
        me_subnet_id = foreman.get_cached_resource_id(
            "api/v2/subnets",
            vm["me_vlan_name"],
        )
        payload["host"]["interfaces_attributes"].extend([
            {
                "primary": True,
                "provision": True,
                "managed": True,
                "name": base_name,
                "domain_id": domain_id,
                "subnet_id": me_subnet_id,
                "ip": vm["me_ip_address"],
                "compute_attributes": {
                    "type": vars.VM_NETWORK_ADAPTER_TYPE,
                    "network": vm["me_vlan_name"],
                },
            },
            {
                "primary": False,
                "provision": False,
                "managed": True,
                "subnet_id": fe_subnet_id,
                "ip": vm["fe_ip_address"],
                "compute_attributes": {
                    "type": vars.VM_NETWORK_ADAPTER_TYPE,
                    "network": vm["fe_vlan_name"],
                },
            },
        ])
    else:
        payload["host"]["interfaces_attributes"].append({
            "primary": True,
            "provision": True,
            "managed": True,
            "name": base_name,
            "domain_id": domain_id,
            "subnet_id": fe_subnet_id,
            "ip": vm["fe_ip_address"],
            "compute_attributes": {
                "type": vars.VM_NETWORK_ADAPTER_TYPE,
                "network": vm["fe_vlan_name"],
            },
        })


def _add_disks(payload, vm):
    """Add system and optional data disks."""
    hostname = vm.get("logical_name", "UNKNOWN")
    volumes = payload["host"]["compute_attributes"]["volumes_attributes"]
    disk_specs = (
        (
            "storage1_disk_size_system",
            "storage1_datastore_system",
            "system",
        ),
        (
            "storage2_disk_size_data",
            "storage2_datastore_data",
            "data",
        ),
    )

    for size_key, datastore_key, label in disk_specs:
        if not is_valid(vm.get(size_key)):
            continue

        if not is_valid(vm.get(datastore_key)):
            raise ValueError(
                "VM {}: {} disk size is defined but {} is missing".format(
                    hostname,
                    label,
                    datastore_key,
                )
            )

        volumes.append({
            "size_gb": int(vm[size_key]),
            "datastore": vm[datastore_key],
            "storage_type": vm[vars.VM_DISK_TYPE_COLUMN],
        })
