import requests
import json
from requests.auth import HTTPBasicAuth
from functions import vars

# Fix Import Loop: Point to the new merged file but alias it as generic
from functions import general as generic
from datetime import datetime, timedelta

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

org_id = generic.get_resource_id(vars.FOREMAN_URL,"api/organizations",vars.USER,vars.PASSWORD,vars.ORG_NAME)
location_id = generic.get_resource_id(vars.FOREMAN_URL,"api/locations",vars.USER,vars.PASSWORD,vars.LOCATION_NAME)
domain_id = generic.get_resource_id(vars.FOREMAN_URL,"api/domains",vars.USER,vars.PASSWORD,vars.DOMAIN_NAME)
subnet_id = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vars.SUBNET_BE)
compute_id = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/compute_resources",vars.USER,vars.PASSWORD,vars.COMPUTE_RESOURCE)
image_id = generic.get_resource_id(vars.FOREMAN_URL,f"api/v2/compute_resources/{compute_id}/images",vars.USER,vars.PASSWORD,vars.IMAGE_NAME)
ansible_job_id = generic.get_resource_id(vars.FOREMAN_URL,f"api/v2/job_templates",vars.USER,vars.PASSWORD,vars.ANSIBLE_JOB_NAME)

def sched_ansible_role(hostname,delay):
    start_time = (datetime.utcnow() + timedelta(seconds=delay)).isoformat() + "Z"
    payload = {
        "job_invocation": {
            "job_template_id": ansible_job_id,
            "target_hosts": hostname,
            "targeting_type": "static_query",
            "search_query": f"name = {hostname}",
            "scheduling": {
                "start_at": start_time
            },
            "description": f"Scheduled Ansible run for {hostname} after provisioning",
            "concurrency_control": {
                "concurrency_level": 1
            }
        }
    }
    try:
        response = requests.post(
            f"{vars.FOREMAN_URL}/api/v2/job_invocations",
            auth=(vars.USER,vars.PASSWORD),
            headers=HEADERS,
            data=json.dumps(payload),
            verify=True
        )

        if response.status_code == 201:
            print(f"Job successfully scheduled to run at {start_time}")
        else:
            print(f"Failed to schedule ansible run job for {hostname}: {response.text}")
    except Exception as e:
        print(f"Error scheduling ansible run job for {hostname}: {e}")

def create(vm):
    payload = create_payload(vm)
    try:
        response = requests.post(
            f"{vars.FOREMAN_URL}/api/hosts", 
            data=json.dumps(payload), 
            auth=(vars.USER,vars.PASSWORD), 
            headers=HEADERS, 
            verify=True
        )
        if response.status_code == 201:
            print(f"Successfully created {vm['logical_name']}")
            generic.create_dns_records(vm)
            sched_ansible_role(vm['logical_name'],vars.ANSIBLE_DELAY)
        else:
            print(f"Failed to create {vm['logical_name']}: {response.text}")

    except Exception as e:
        print(f"Error processing row for {vm['logical_name']}: {e}")

def create_payload(vm):
    payload = {
        "host": {
            "name": vm["logical_name"],
            "hostgroup_id":generic.get_resource_id(vars.FOREMAN_URL,"api/v2/hostgroups",vars.USER,vars.PASSWORD,generic.gethostgroup(vm["subsystems"],vm["function"],vm["variation"])),
            "compute_resource_id": compute_id,
            "image_id": vars.IMAGE_NAME,
            "provision_method": "image",
            "managed": True,
            "path": vm["vm_folder"],
            "compute_attributes": {
                "cpus": int(vm["cpu"]),
                "memory_gb": int(vm["ram_(gb)"]),
                "start": "1",
                "volumes_attributes": []
            },
            "interfaces_attributes": [],
            "host_parameters_attributes": generic.gethost_parameters(vm["foreman_parameters"], vm.get("ntp1", "NODATAFOUND"), vm.get("ntp2", "NODATAFOUND"))
        }
    }
    if vm["fe_ip_address"] != "N.A" and vm["fe_ip_address"] != "NODATAFOUND" and vm["me_ip_address"] != "N.A" and vm["me_ip_address"] != "NODATAFOUND":
        interface_me = {
            "primary": True,
            "provision": True,
            "managed": True,
            "name": str(vm["logical_name"]).replace("." + vm["domain_name"],""),
            "domain_id": generic.get_resource_id(vars.FOREMAN_URL,"api/domains",vars.USER,vars.PASSWORD,vm["domain_name"]),
            "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vm["me_vlan_name"]),
            "ip": vm["me_ip_address"],
            "compute_attributes": {
                "type": "VirtualVmxnet3",
                "network": vm["me_vlan_name"]
            }
        }
        interface_fe = {
            "primary": False,
            "provision": False,
            "managed": True,
            "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vm["fe_vlan_name"]),
            "ip": vm["fe_ip_address"],
            "compute_attributes": {
                "type": "VirtualVmxnet3",
                "network": vm["fe_vlan_name"]
            }
        }
        payload["host"]["interfaces_attributes"].append(interface_me)
        payload["host"]["interfaces_attributes"].append(interface_fe)
    if vm["fe_ip_address"] != "N.A" and vm["fe_ip_address"] != "NODATAFOUND" and (vm["me_ip_address"] == "N.A" or vm["me_ip_address"] == "NODATAFOUND"):
        interface_fe = {
            "primary": True,
            "provision": True,
            "managed": True,
            "name": str(vm["logical_name"]).replace("." + vm["domain_name"],""),
            "domain_id": generic.get_resource_id(vars.FOREMAN_URL,"api/domains",vars.USER,vars.PASSWORD,vm["domain_name"]),
            "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vm["fe_vlan_name"]),
            "ip": vm["fe_ip_address"],
            "compute_attributes": {
                "type": "VirtualVmxnet3",
                "network": vm["fe_vlan_name"]
            }
        }
        payload["host"]["interfaces_attributes"].append(interface_fe)
    if vm["storage1_disk_size_system"] != "NODATAFOUND":
        disk1 = {
            "size_gb": int(vm["storage1_disk_size_system"]),
            "datastore": vm["storage1_datastore_system"],
            "storage_type": vm["virtual_disk_type"]
        }
        payload["host"]["compute_attributes"]["volumes_attributes"].append(disk1)
    if vm["storage2_disk_size_data"] != "NODATAFOUND":
        disk2 = {
            "size_gb": int(vm["storage2_disk_size_data"]),
            "datastore": vm["storage2_datastore_data"],
            "storage_type": vm["virtual_disk_type"]
        }
        payload["host"]["compute_attributes"]["volumes_attributes"].append(disk2)
    return(payload)