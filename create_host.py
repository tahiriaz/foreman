import requests
from requests.auth import HTTPBasicAuth
from functions import general

# Foreman API configuration
FOREMAN_URL = "https://idsfrk02.mak.iss"
USER = "localadmin"
PASSWORD = "Th@les01"
DOMAIN_NAME = "mak.iss"
ORG_NAME = "Thales KSA"
LOCATION_NAME = "Shamiyah Project"
SUBNET_FE = "mtr_tvs_nvr_fe"
SUBNET_BE = "mtr_tvs_nvr_be"
SUBNET_ME = "mtr_tvs_nvr_me"
HOSTGROUP_NAME = "Default Host Group"

# Execute
org_id = general.get_organization_id(FOREMAN_URL,USER,PASSWORD,ORG_NAME)
if org_id:
    print(f"Location ID for '{ORG_NAME}': {org_id}")

location_id = general.get_location_id(FOREMAN_URL,USER,PASSWORD,LOCATION_NAME)
if location_id:
    print(f"Location ID for '{LOCATION_NAME}': {location_id}")

domain_id = general.get_domain_id(FOREMAN_URL,USER,PASSWORD,DOMAIN_NAME)
if domain_id:
    print(f"Domain ID for '{DOMAIN_NAME}' is: {domain_id}")

subnet_id = general.get_subnet_id(FOREMAN_URL,USER,PASSWORD,SUBNET_BE)
if subnet_id:
    print(f"Subnet ID for '{SUBNET_BE}' is: {subnet_id}")

hostgroup_id = general.get_hostgroup_id(FOREMAN_URL,USER,PASSWORD,HOSTGROUP_NAME)
if hostgroup_id:
    print(f"Hostgroup ID for '{HOSTGROUP_NAME}' is: {hostgroup_id}")