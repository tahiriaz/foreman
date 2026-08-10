import os

FOREMAN_URL = "https://idsfrk02.mak.iss"
USER = "localadmin"
PASSWORD = "Th@les01"
DOMAIN_NAME = "mak.iss"
ORG_NAME = "Thales KSA"
LOCATION_NAME = "Shamiyah Project"
SUBNET_FE = "mtr_tvs_nvr_fe"
SUBNET_BE = "mtr_tvs_nvr_be"
SUBNET_ME = "mtr_tvs_nvr_me"
HOSTGROUP_NAME = "TVS_VMs"
COMPUTE_RESOURCE = "ISS vDC"
IMAGE_NAME = "RHEL 8.10"
VSTORAGE_TYPE = "thin"
ANSIBLE_JOB_NAME = "Ansible Roles - Ansible Default"
ANSIBLE_DELAY = 180
DNS_SERVER = "10.130.2.11"
DNS_SERVER_USER = "MAK.ISS\Administrator"
DNS_SERVER_PASS = "Th@les01"
DNS_DIR = os.path.dirname(os.path.abspath(__file__))
DNS_SCRIPT = "add_dns_records.ps1"
DNS_FILENAME = "dns_vm.csv"
MTR_PXE_SUBNET = "mtr_nvr_pxe"
RTR_PXE_SUBNET = "rtr_nvr_pxe"

hg_map = {
        "tvsvms" : "TVS",
        "tvsnvr" : "NVR",
        "cwdvca" : "VCA",
        "cwdsdp" : "SDP",
        "ucscis" : "UCS",
        "ucsimg" : "UCS",
        "ucscal" : "UCS",
        "acscem" : "ACS",
        "infsrv" : "IT",
        "infvir" : "IT",
        "infitc" : "IT",
        "infims" : "IT",
        "infics" : "IT",
        "infids" : "IT",
        "infsup" : "Supervision"
}