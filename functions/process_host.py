import requests
import json
from requests.auth import HTTPBasicAuth
from functions import vars
from functions import generic

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


domain_id = generic.get_resource_id(vars.FOREMAN_URL,"api/domains",vars.USER,vars.PASSWORD,vars.DOMAIN_NAME)
subnet_id = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vars.SUBNET_BE)

def create(host):
   payload = create_payload(host)
   try:
            response = requests.post(
                    f"{vars.FOREMAN_URL}/api/hosts", 
                    data=json.dumps(payload), 
                    auth=(vars.USER,vars.PASSWORD), 
                    headers=HEADERS, 
                    verify=True
            )
            if response.status_code == 201:
                    print(f"Successfully created {host['hostname']}")
                    # Temporary disabled creating DNS records for physical hosts
                    # generic.create_dns_records(host)
            else:
                    print(f"Failed to create {host['hostname']}: {response.text}")

   except Exception as e:
        print(f"Error processing row for {host['hostname']}: {e}")


def create_payload(host):
        payload = {
            "host": {
                "name": host["hostname"],
                "hostgroup_id":generic.get_resource_id(vars.FOREMAN_URL,"api/v2/hostgroups",vars.USER,vars.PASSWORD,generic.gethostgroup(host["subsystems"],host["function"])),
                "build": True,
                "managed": True,
                "host_parameters_attributes": generic.gethost_parameters(host["foreman_parameters"],host["ntp1"],host["ntp2"]),
                "interfaces_attributes": []
            }
        }
        payload_i = add_interface(payload,host)
        return payload_i

def add_interface(payload,host):
      interfaces = []
      ### Bond 0
      if host["nic0_name"] != "N.A" and host["nic0_name"] != "NODATAFOUND":
            if host["nic1_name"] != "N.A" and host["nic1_name"] != "NODATAFOUND":
                  if host["bond0_name"] != "N.A" and host["bond0_name"] != "NODATAFOUND":
                        nic1 = {
                                "identifier": host["nic0_name"], 
                                "type": "interface",
                                "mac": host["nic0_mac"],
                                "managed": True,
                                "provision": True,
                                "subnet_id" : generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["nic0_pxe_subnet_name"]),
                                "domain_id" : domain_id,
                                "primary": False
                            }
                        nic2 = {
                                "identifier": host["nic1_name"], 
                                "type": "interface",
                                "mac": host["nic1_mac"],
                                "managed": True,
                                "primary": False
                            }
                        nic3 = {
                                "identifier": host["bond0_name"], 
                                "type": "bond",
                                "mode": host["bond0_type"],
                                "attached_devices": host["bond0_devs"],
                                "managed": True,
                                "primary": False
                            }
                        if host["fe_interface_type"] == "bond" and host["fe_attach_to"] == "bond0":
                              nic3["ip"] = host["fe_ip_address"]
                              nic3["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["fe_vlan_name"])
                              nic3["domain_id"] = domain_id
                        if host["me_interface_type"] == "bond" and host["me_attach_to"] == "bond0":
                              nic3["ip"] = host["me_ip_address"]
                              nic3["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["me_vlan_name"])
                              nic3["domain_id"] = domain_id
                        if host["be_interface_type"] == "bond" and host["be_attach_to"] == "bond0":
                              nic3["ip"] = host["be_ip_address"]
                              nic3["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["be_vlan_name"])
                              nic3["domain_id"] = domain_id
                        if host["cl_interface_type"] == "bond" and host["cl_attach_to"] == "bond0":
                              nic3["ip"] = host["cl_ip_address"]
                              nic3["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["cl_vlan_name"])
                              nic3["domain_id"] = domain_id
                        interfaces.append(nic1)
                        interfaces.append(nic2)
                        interfaces.append(nic3)

      ### Bond 1
      if host["nic2_name"] != "N.A" and host["nic2_name"] != "NODATAFOUND":
            if host["nic3_name"] != "N.A" and host["nic3_name"] != "NODATAFOUND":
                  if host["bond1_name"] != "N.A" and host["bond1_name"] != "NODATAFOUND":
                        nic4 = {
                                "identifier": host["nic2_name"], 
                                "type": "interface",
                                "mac": host["nic2_mac"],
                                "managed": True,
                                "primary": False
                            }
                        nic5 = {
                                "identifier": host["nic3_name"], 
                                "type": "interface",
                                "mac": host["nic3_mac"],
                                "managed": True,
                                "primary": False
                            }
                        nic6 = {
                                "identifier": host["bond1_name"], 
                                "type": "bond",
                                "mode": host["bond1_type"],
                                "attached_devices": host["bond1_devs"],
                                "managed": True,
                                "primary": False
                            }
                        if host["fe_interface_type"] == "bond" and host["fe_attach_to"] == "bond1":
                              nic6["ip"] = host["fe_ip_address"]
                              nic6["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["fe_vlan_name"])
                              nic6["domain_id"] = domain_id
                        if host["me_interface_type"] == "bond" and host["me_attach_to"] == "bond1":
                              nic6["ip"] = host["me_ip_address"]
                              nic6["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["me_vlan_name"])
                              nic6["domain_id"] = domain_id
                        if host["be_interface_type"] == "bond" and host["be_attach_to"] == "bond1":
                              nic6["ip"] = host["be_ip_address"]
                              nic6["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["be_vlan_name"])
                              nic6["domain_id"] = domain_id
                        if host["cl_interface_type"] == "bond" and host["cl_attach_to"] == "bond1":
                              nic6["ip"] = host["cl_ip_address"]
                              nic6["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["cl_vlan_name"])
                              nic6["domain_id"] = domain_id
                        interfaces.append(nic4)
                        interfaces.append(nic5)
                        interfaces.append(nic6)                        

      ### Bond 2
      if host["nic4_name"] != "N.A" and host["nic4_name"] != "NODATAFOUND":
            if host["nic5_name"] != "N.A" and host["nic5_name"] != "NODATAFOUND":
                  if host["bond2_name"] != "N.A" and host["bond2_name"] != "NODATAFOUND":
                        nic7 = {
                                "identifier": host["nic4_name"], 
                                "type": "interface",
                                "mac": host["nic4_mac"],
                                "managed": True,
                                "primary": False
                            }
                        nic8 = {
                                "identifier": host["nic5_name"], 
                                "type": "interface",
                                "mac": host["nic5_mac"],
                                "managed": True,
                                "primary": False
                            }
                        nic9 = {
                                "identifier": host["bond2_name"], 
                                "type": "bond",
                                "mode": host["bond2_type"],
                                "attached_devices": host["bond2_devs"],
                                "managed": True,
                                "primary": False
                            }
                        if host["fe_interface_type"] == "bond" and host["fe_attach_to"] == "bond2":
                              nic9["ip"] = host["fe_ip_address"]
                              nic9["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["fe_vlan_name"])
                              nic9["domain_id"] = domain_id
                        if host["me_interface_type"] == "bond" and host["me_attach_to"] == "bond2":
                              nic9["ip"] = host["me_ip_address"]
                              nic9["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["me_vlan_name"])
                              nic9["domain_id"] = domain_id
                        if host["be_interface_type"] == "bond" and host["be_attach_to"] == "bond2":
                              nic9["ip"] = host["be_ip_address"]
                              nic9["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["be_vlan_name"])
                              nic9["domain_id"] = domain_id
                        if host["cl_interface_type"] == "bond" and host["cl_attach_to"] == "bond2":
                              nic9["ip"] = host["cl_ip_address"]
                              nic9["subnet_id"] = generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["cl_vlan_name"])
                              nic9["domain_id"] = domain_id
                        interfaces.append(nic7)
                        interfaces.append(nic8)
                        interfaces.append(nic9)
      ### FrontEnd
      if host["fe_ip_address"] != "N.A" and host["fe_ip_address"] != "NODATAFOUND" and host["fe_interface_type"] == "vlan":
            nic10 ={
                    "identifier": host["fe_interface_name"],
                    "type": "interface",
                    "tag": int(host["fe_vlan_id"]),
                    "attached_to": host["fe_attach_to"],
                    "ip": host["fe_ip_address"],
                    "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["fe_vlan_name"]),
                    "domain_id": domain_id,
                    "managed": True,
                    "virtual": True,
                    "primary": False
            }
            interfaces.append(nic10)

      ### MiddleEnd
      if host["me_ip_address"] != "N.A" and host["me_ip_address"] != "NODATAFOUND" and host["me_interface_type"] == "vlan":
            nic11 ={
                    "identifier": host["me_interface_name"],
                    "type": "interface",
                    "tag": int(host["me_vlan_id"]),
                    "attached_to": host["me_attach_to"],
                    "ip": host["me_ip_address"],
                    "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["me_vlan_name"]),
                    "domain_id": domain_id,
                    "managed": True,
                    "virtual": True,
                    "primary": True
            }
            interfaces.append(nic11)        

      ### BackEnd
      if host["be_ip_address"] != "N.A" and host["be_ip_address"] != "NODATAFOUND" and host["be_interface_type"] == "vlan":
            nic12 ={
                    "identifier": host["be_interface_name"],
                    "type": "interface",
                    "tag": int(host["be_vlan_id"]),
                    "attached_to": host["be_attach_to"],
                    "ip": host["be_ip_address"],
                    "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["be_vlan_name"]),
                    "domain_id": domain_id,
                    "managed": True,
                    "virtual": True,
                    "primary": False
            }
            interfaces.append(nic12)

      ### Cluster
      if host["cl_ip_address"] != "N.A" and host["cl_ip_address"] != "NODATAFOUND" and host["cl_interface_type"] == "vlan":
            nic13 ={
                    "identifier": host["cl_interface_name"],
                    "type": "interface",
                    "tag": int(host["cl_vlan_id"]),
                    "attached_to": host["cl_attach_to"],
                    "ip": host["cl_ip_address"],
                    "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,host["cl_vlan_name"]),
                    "domain_id": domain_id,
                    "managed": True,
                    "virtual": True,
                    "primary": False
            }
            interfaces.append(nic13)

      payload["host"]["interfaces_attributes"] = interfaces
      return payload
# def create(vm):
#         payload = create_payload(vm)
#         try:
#                 response = requests.post(
#                         f"{vars.FOREMAN_URL}/api/hosts", 
#                         data=json.dumps(payload), 
#                         auth=(vars.USER,vars.PASSWORD), 
#                         headers=HEADERS, 
#                         verify=True
#                 )
#                 if response.status_code == 201:
#                         print(f"Successfully created {vm['logical_name']}")
#                         generic.create_dns_records(vm)
#                         sched_ansible_role(vm['logical_name'],vars.ANSIBLE_DELAY)
#                 else:
#                         print(f"Failed to create {vm['logical_name']}: {response.text}")

#         except Exception as e:
#             print(f"Error processing row for {vm['logical_name']}: {e}")



# def create_payload(vm):
#         payload = {
#             "host": {
#                 "name": vm["logical_name"],
#                 "hostgroup_id":generic.get_resource_id(vars.FOREMAN_URL,"api/v2/hostgroups",vars.USER,vars.PASSWORD,gethostgroup(vm["subsystems"],vm["function"])),
#                 "compute_resource_id": compute_id,
#                 "image_id": vars.IMAGE_NAME,
#                 "provision_method": "image",
#                 "managed": True,
#                 "path": vm["vm_folder"],
#                 "compute_attributes": {
#                     "cpus": int(vm["cpu"]),
#                     "memory_gb": int(vm["ram_(gb)"]),
#                     "start": "1",
#                     "volumes_attributes": []
#                 },
#                 "interfaces_attributes": [],
#                 "host_parameters_attributes": gethost_parameters(vm["foreman_parameters"])
#             }
#         }
#         if vm["fe_ip_address"] != "N.A" and vm["fe_ip_address"] != "NODATAFOUND" and vm["me_ip_address"] != "N.A" and vm["me_ip_address"] != "NODATAFOUND":
#                 interface_me = {
#                         "primary": True,
#                         "provision": True,
#                         "managed": True,
#                         "name": str(vm["logical_name"]).replace("." + vm["domain_name"],""),
#                         "domain_id": generic.get_resource_id(vars.FOREMAN_URL,"api/domains",vars.USER,vars.PASSWORD,vm["domain_name"]),
#                         "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vm["me_vlan_name"]),
#                         "ip": vm["me_ip_address"],
#                         "compute_attributes": {
#                             "type": "VirtualVmxnet3",
#                             "network": vm["me_vlan_name"]
#                         }
#                 }
#                 interface_fe = {
#                         "primary": False,
#                         "provision": False,
#                         "managed": True,
#                         "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vm["fe_vlan_name"]),
#                         "ip": vm["fe_ip_address"],
#                         "compute_attributes": {
#                             "type": "VirtualVmxnet3",
#                             "network": vm["fe_vlan_name"]
#                         }
#                 }
#                 payload["host"]["interfaces_attributes"].append(interface_me)
#                 payload["host"]["interfaces_attributes"].append(interface_fe)
#         if vm["fe_ip_address"] != "N.A" and vm["fe_ip_address"] != "NODATAFOUND" and (vm["me_ip_address"] == "N.A" or vm["me_ip_address"] == "NODATAFOUND"):
#                 interface_fe = {
#                         "primary": True,
#                         "provision": True,
#                         "managed": True,
#                         "name": str(vm["logical_name"]).replace("." + vm["domain_name"],""),
#                         "domain_id": generic.get_resource_id(vars.FOREMAN_URL,"api/domains",vars.USER,vars.PASSWORD,vm["domain_name"]),
#                         "subnet_id": generic.get_resource_id(vars.FOREMAN_URL,"api/v2/subnets",vars.USER,vars.PASSWORD,vm["fe_vlan_name"]),
#                         "ip": vm["fe_ip_address"],
#                         "compute_attributes": {
#                             "type": "VirtualVmxnet3",
#                             "network": vm["fe_vlan_name"]
#                         }
#                 }
#                 payload["host"]["interfaces_attributes"].append(interface_fe)
#         if vm["storage1_disk_size_system"] != "NODATAFOUND":
#                 disk1 = {
#                         "size_gb": int(vm["storage1_disk_size_system"]),
#                         "datastore": vm["storage1_datastore_system"],
#                         "storage_type": vm["virtual_disk_type"]
#                 }
#                 payload["host"]["compute_attributes"]["volumes_attributes"].append(disk1)
#         if vm["storage2_disk_size_data"] != "NODATAFOUND":
#                 disk2 = {
#                         "size_gb": int(vm["storage2_disk_size_data"]),
#                         "datastore": vm["storage2_datastore_data"],
#                         "storage_type": vm["virtual_disk_type"]
#                 }
#                 payload["host"]["compute_attributes"]["volumes_attributes"].append(disk2)
#         return(payload)