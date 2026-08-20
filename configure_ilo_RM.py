#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import subprocess
import urllib3
import requests
import pandas as pd
from pathlib import Path

# Disable insecure request warnings for self-signed iLO certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================================
# CREDENTIALS & LICENSING
# ============================================================================
ILO_LOGIN = "Administrator"
ILO_PASSWORD = "Th@les01"
ILO_ADVANCED_LICENSE_KEY = "35SCR-RYLML-CBK7N-TD3B9-GGBW2"

FENCE_USER_NAME = "Pacemaker Fence"
FENCE_USER_LOGIN = "hpilofence"
FENCE_USER_PASSWORD = "Th@les01"

IPMI_PORT = 623
ILO_DOMAIN = "mak.iss"

# LDAP User Search Contexts (Base DNs)
DIR_USER_CONTEXT_1 = "OU=IT,OU=ISS,DC=mak,DC=iss"
DIR_USER_CONTEXT_2 = "CN=Users,DC=mak,DC=iss"
DIR_USER_CONTEXT_3 = "CN=Builtin,DC=mak,DC=iss"
DIR_USER_CONTEXT_4 = "@mak.iss"

AD_GROUP_DN = "CN=ILOAdmins,OU=Roles,OU=IT,OU=ISS,DC=mak,DC=iss"

# ============================================================================
# EXCEL DATA EXTRACTION SETTINGS
# ============================================================================
EQUIPMENT_TYPES = ["NVR", "VCA", "ESXi"]
START_ROW = 1026
END_ROW = 1037

SCOPE_SETTINGS = {
    "MTR": {
        "PRIMARY_DNS": "10.130.2.11",
        "SECONDARY_DNS": "10.130.2.12",
        "DIRECTORY_SERVER": "INFCOSADU001MP.mak.iss"
    },
    "RTR": {
        "PRIMARY_DNS": "10.130.4.11",
        "SECONDARY_DNS": "10.130.4.12",
        "DIRECTORY_SERVER": "INFCOSADU001RP.mak.iss"
    }
}

# ============================================================================
# DEBUG & PATHS
# ============================================================================
DEBUG_MODE = False
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "Templates"
EXCEL_FILE = TEMPLATE_DIR / "Resource List-v7.6.xlsx"
CERT_FILE = TEMPLATE_DIR / "iss_root_ca.crt"

# ============================================================================
# REDFISH SETTINGS
# ============================================================================
REDFISH_PORT = 443
CONNECT_TIMEOUT = 15
REQUEST_TIMEOUT = 30
RETRY_COUNT = 3
RETRY_DELAY = 5

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_reachable(ip):
    print("  -> Pinging {}...".format(ip))
    if os.name == "nt":
        command = ["ping", "-n", "2", "-w", "500", str(ip)]
    else:
        command = ["ping", "-c", "2", "-W", "1", str(ip)]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def response_is_success(response):
    if response.status_code < 200 or response.status_code >= 300:
        return False
    try:
        data = response.json()
    except Exception:
        return True
    error = data.get("error")
    if not error:
        return True
    extended_info = error.get("@Message.ExtendedInfo", [])
    for item in extended_info:
        message_id = item.get("MessageId", "")
        if message_id.endswith(".Success") or "ResetRequired" in message_id or "ResetInProgress" in message_id:
            return True
    return False

def check_reset_required(response):
    return "ResetRequired" in response.text or "ResetInProgress" in response.text

def get_redfish_error(response):
    try:
        data = response.json()
        error = data.get("error", {})
        messages = error.get("@Message.ExtendedInfo", [])
        result = []
        for message in messages:
            message_id = message.get("MessageId", "")
            message_args = message.get("MessageArgs", [])
            if message_args:
                result.append("{}: {}".format(message_id, ", ".join([str(x) for x in message_args])))
            else:
                result.append(message_id)
        if result:
            return "; ".join(result)
        return error.get("message", response.text)
    except Exception:
        return response.text

def safe_debug_payload(payload):
    if not isinstance(payload, dict):
        return payload
    try:
        result = json.loads(json.dumps(payload))
    except Exception:
        return payload
    sensitive_keys = ["Password", "password", "LicenseKey", "Certificate", "CertificateString"]
    def scrub(obj):
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key in sensitive_keys:
                    obj[key] = "***REDACTED***"
                else:
                    scrub(obj[key])
        elif isinstance(obj, list):
            for item in obj:
                scrub(item)
    scrub(result)
    return result

# ============================================================================
# REDFISH CLIENT
# ============================================================================

class RedfishClient(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.base_url = "https://{}:{}/redfish/v1".format(ip, REDFISH_PORT)
        
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "OData-Version": "4.0",
            "Connection": "close"
        })
        self.token = None
        self.manager_uri = None
        self.system_uri = None

    def login(self):
        print("  -> Authenticating and establishing Redfish session...")
        payload = {"UserName": self.username, "Password": self.password}
        url = self.base_url + "/SessionService/Sessions"
        
        try:
            response = self.session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            if DEBUG_MODE:
                print("\n    [DEBUG] POST /SessionService/Sessions")
                print("    [DEBUG] STATUS: {}".format(response.status_code))
                
            if response.status_code in [200, 201]:
                self.token = response.headers.get("X-Auth-Token")
                if self.token:
                    self.session.headers.update({"X-Auth-Token": self.token})
                    self.session.auth = None
                    print("  -> Redfish session established (Token-Based).")
                return True
                
            print("  [WARNING] Token login failed. Trying Basic Authentication...")
            self.session.auth = (self.username, self.password)
            response = self.session.get(self.base_url + "/", timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                print("  -> Basic Authentication successful.")
                return True
            return False
            
        except requests.exceptions.RequestException as exc:
            print("  [ERROR] Authentication connection failed: {}".format(exc))
            return False

    def logout(self):
        if self.token: pass
        self.session.close()

    def _request(self, method, endpoint, payload=None, retries=RETRY_COUNT):
        if endpoint.startswith("/redfish/v1"):
            url = "https://{}:{}".format(self.ip, REDFISH_PORT) + endpoint
        else:
            url = self.base_url + (endpoint if endpoint.startswith("/") else "/" + endpoint)

        last_exception = None

        for attempt in range(1, retries + 1):
            try:
                if DEBUG_MODE:
                    print("\n    [DEBUG] {} {}".format(method, url))
                    if payload is not None:
                        print("    [DEBUG] PAYLOAD: {}".format(json.dumps(safe_debug_payload(payload), indent=2)))

                if method == "GET":
                    response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                elif method == "POST":
                    response = self.session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
                elif method == "PATCH":
                    response = self.session.patch(url, json=payload, timeout=REQUEST_TIMEOUT)
                elif method == "DELETE":
                    response = self.session.delete(url, timeout=REQUEST_TIMEOUT)

                if DEBUG_MODE:
                    print("    [DEBUG] STATUS: {}".format(response.status_code))
                    print("    [DEBUG] RESPONSE: {}".format(response.text))

                return response

            except requests.exceptions.RequestException as exc:
                last_exception = exc
                if attempt < retries:
                    time.sleep(RETRY_DELAY)
                else:
                    raise last_exception

        raise last_exception

    def get(self, endpoint): return self._request("GET", endpoint)
    def post(self, endpoint, payload): return self._request("POST", endpoint, payload)
    def patch(self, endpoint, payload): return self._request("PATCH", endpoint, payload)

    def discover_resources(self):
        root = self.get("/")
        data = root.json()
        
        manager_collection = data.get("Managers", {}).get("@odata.id")
        system_collection = data.get("Systems", {}).get("@odata.id")

        managers = self.get(manager_collection)
        manager_data = managers.json()
        self.manager_uri = manager_data.get("Members", [])[0].get("@odata.id")

        systems = self.get(system_collection)
        system_data = systems.json()
        self.system_uri = system_data.get("Members", [])[0].get("@odata.id")

# ============================================================================
# CONFIGURATION TASKS
# ============================================================================

def apply_license(client):
    print("  -> [STEP 1] Checking iLO Advanced License...")
    endpoint = client.manager_uri.rstrip('/') + "/LicenseService/"
    response = client.get(endpoint)
    
    if response.status_code == 200:
        data = response.json()
        for member in data.get("Members", []):
            lic_res = client.get(member.get("@odata.id"))
            if lic_res.status_code == 200:
                lic_data = lic_res.json()
                if "Advanced" in str(lic_data.get("License", "")):
                    print("  -> iLO Advanced license already installed.")
                    return True, False

    print("  -> iLO Advanced license missing. Applying license...")
    payload = {"LicenseKey": ILO_ADVANCED_LICENSE_KEY}
    response = client.post(endpoint, payload)
    
    if response_is_success(response):
        print("  [SUCCESS] iLO Advanced license applied.")
        time.sleep(5)
        return True, False
        
    print("  [ERROR] License installation failed.")
    return False, False

def apply_fencing_user(client):
    print("  -> [STEP 2] Checking for fencing user '{}'...".format(FENCE_USER_LOGIN))
    response = client.get("/AccountService/Accounts/")
    
    if response.status_code == 200:
        for member in response.json().get("Members", []):
            acc_res = client.get(member.get("@odata.id"))
            if acc_res.status_code == 200 and acc_res.json().get("UserName") == FENCE_USER_LOGIN:
                print("  -> Fencing user '{}' already exists.".format(FENCE_USER_LOGIN))
                return True, False

    print("  -> Creating fencing user...")
    payload = {
        "UserName": FENCE_USER_LOGIN,
        "Password": FENCE_USER_PASSWORD,
        "Oem": {
            "Hpe": {
                "LoginName": FENCE_USER_LOGIN,
                "Privileges": {
                    "LoginPriv": True,
                    "VirtualPowerAndResetPriv": True,
                    "RemoteConsolePriv": False,
                    "VirtualMediaPriv": False,
                    "UserConfigPriv": False,
                    "iLOConfigPriv": False
                }
            }
        }
    }
    response = client.post("/AccountService/Accounts/", payload)
    
    if response_is_success(response):
        print("  [SUCCESS] Fencing user created.")
        return True, False
    print("  [ERROR] Fencing user creation failed.")
    return False, False

def configure_ldap(client, scope_data):
    print("  -> [STEP 3] Configuring Generic LDAP (DefaultSchema) & Group Mappings...")
    overall_success = True
    needs_reset = False
    
    ldap_payload = {
        "ActiveDirectory": {
            "ServiceEnabled": False
        },
        "LDAP": {
            "ServiceEnabled": True,
            "ServiceAddresses": [scope_data["DIRECTORY_SERVER"]],
            "Authentication": {
                "AuthenticationType": "UsernameAndPassword"
            },
            "LDAPService": {
                "SearchSettings": {
                    "BaseDistinguishedNames": [
                        DIR_USER_CONTEXT_1,
                        DIR_USER_CONTEXT_2,
                        DIR_USER_CONTEXT_3,
                        DIR_USER_CONTEXT_4
                    ]
                }
            },
            "RemoteRoleMapping": [
                {
                    "LocalRole": "Administrator",
                    "RemoteGroup": AD_GROUP_DN
                }
            ]
        },
        "Oem": {
            "Hpe": {
                "DirectorySettings": {
                    "LdapAuthenticationMode": "DefaultSchema"
                }
            }
        }
    }
    
    response = client.patch("/AccountService/", ldap_payload)
    if check_reset_required(response): needs_reset = True
    
    if response_is_success(response):
        print("  [SUCCESS] Generic LDAP settings and Search Contexts applied.")
    else:
        print("  [ERROR] LDAP configuration failed: {}".format(get_redfish_error(response)))
        overall_success = False

    return overall_success, needs_reset

def configure_ldap_certificate(client):
    print("  -> [STEP 4] Importing LDAP CA certificate...")
    if not CERT_FILE.is_file():
        print("  [WARNING] LDAP CA certificate not found at {}.".format(CERT_FILE))
        return False, False

    try:
        with open(CERT_FILE, "r") as cert_file:
            certificate = cert_file.read().strip()
    except Exception as exc:
        print("  [ERROR] Failed to read certificate file: {}".format(exc))
        return False, False

    # Attempt 1: The Modern Standard Redfish Collection Endpoint [1]
    cert_endpoint_std = "/AccountService/ExternalAccountProviders/LDAP/Certificates/"
    payload_std = {
        "CertificateString": certificate,
        "CertificateType": "PEM"
    }
    
    cert_res = client.post(cert_endpoint_std, payload_std)
    
    if response_is_success(cert_res):
        print("  [SUCCESS] LDAP CA certificate imported via standard Redfish endpoint.")
        return True, check_reset_required(cert_res)
        
    if DEBUG_MODE:
        print("  [WARNING] Standard Redfish endpoint failed ({}). Trying OEM fallback...".format(cert_res.status_code))

    # Attempt 2: OEM SecurityService Endpoint [2]
    cert_endpoint_oem = client.manager_uri.rstrip('/') + "/SecurityService/Actions/Oem/Hpe/HpeiLOSecurityService.ImportDirectoryCACertificate"
    payload_oem = {"Certificate": certificate}
    cert_res_oem = client.post(cert_endpoint_oem, payload_oem)
    
    if response_is_success(cert_res_oem):
        print("  [SUCCESS] LDAP CA certificate imported via OEM endpoint.")
        return True, check_reset_required(cert_res_oem)
        
    print("  [ERROR] LDAP CA certificate import failed on all endpoints.")
    print("  [ERROR] Final response: {}".format(get_redfish_error(cert_res_oem)))
    return False, False

def configure_server_identification(client, server_name, server_fqdn):
    print("  -> [STEP 5] Configuring Server Identification (OS Name & FQDN)...")
    endpoint = client.system_uri.rstrip('/') + "/"
    
    payload = {
        "HostName": server_name,
        "Oem": {
            "Hpe": {
                "ServerFQDN": server_fqdn
            }
        }
    }
    
    response = client.patch(endpoint, payload)
    success = response_is_success(response)
    needs_reset = check_reset_required(response)
    
    if success:
        print("  [SUCCESS] Server Identification (Name/FQDN) configured.")
    else:
        print("  [ERROR] Server Identification failed: {}".format(get_redfish_error(response)))
    return success, needs_reset

def configure_ilo_network(client, server_fqdn, scope_data):
    print("  -> [STEP 6] Configuring iLO Network (Dedicated Port Hostname & DNS)...")
    ethernet_uri = client.manager_uri.rstrip('/') + "/EthernetInterfaces/1/"

    payload_dhcp = {
        "Oem": {
            "Hpe": {
                "DHCPv4": {"UseDNSServers": False, "UseDomainName": False, "UseNTPServers": False},
                "DHCPv6": {"UseDNSServers": False, "UseDomainName": False, "UseNTPServers": False}
            }
        }
    }
    client.patch(ethernet_uri, payload_dhcp)

    ilo_short_name = server_fqdn.split('.')[0]
    payload_network = {
        "HostName": ilo_short_name,
        "StaticNameServers": [scope_data["PRIMARY_DNS"], scope_data["SECONDARY_DNS"]],
        "Oem": {
            "Hpe": {
                "DomainName": ILO_DOMAIN
            }
        }
    }
    response = client.patch(ethernet_uri, payload_network)
    success = response_is_success(response)
    needs_reset = check_reset_required(response)
    
    if success:
        print("  [SUCCESS] iLO Network Hostname / DNS configured.")
    else:
        print("  [ERROR] Network configuration failed: {}".format(get_redfish_error(response)))
    return success, needs_reset

def configure_ipmi(client):
    print("  -> [STEP 7] Enabling IPMI over LAN on port {}...".format(IPMI_PORT))
    endpoint = client.manager_uri.rstrip('/') + "/NetworkProtocol/"
    payload = {"IPMI": {"ProtocolEnabled": True, "Port": IPMI_PORT}}
    
    response = client.patch(endpoint, payload)
    success = response_is_success(response)
    needs_reset = check_reset_required(response)
    
    if success:
        print("  [SUCCESS] IPMI over LAN enabled.")
    else:
        print("  [ERROR] IPMI configuration failed.")
    return success, needs_reset

def set_boot_order(client):
    print("  -> [STEP 8] Setting one-time UEFI network/PXE boot...")
    endpoint = client.system_uri.rstrip('/') + "/"
    payload = {
        "Boot": {
            "BootSourceOverrideTarget": "Pxe",
            "BootSourceOverrideEnabled": "Once"
        }
    }
    response = client.patch(endpoint, payload)
    success = response_is_success(response)
    needs_reset = check_reset_required(response)
    
    if success:
        print("  [SUCCESS] One-time PXE/network boot configured.")
    else:
        print("  [ERROR] One-time PXE boot configuration failed.")
    return success, needs_reset

def trigger_ilo_reset(client):
    print("\n  -> Triggering iLO Reset to apply pending configurations...")
    endpoint = client.manager_uri.rstrip('/') + "/Actions/Manager.Reset"
    payload = {"ResetType": "ForceRestart"}
    
    response = client.post(endpoint, payload)
    if response_is_success(response):
        print("  [SUCCESS] iLO reset triggered. It will be temporarily unreachable.")
    else:
        print("  [ERROR] Failed to trigger iLO reset: {}".format(get_redfish_error(response)))

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "=" * 78)
    print("HPE ProLiant DL380 Gen10+ / iLO 5 Redfish Configuration")
    print("=" * 78 + "\n")

    if not EXCEL_FILE.is_file():
        print("ERROR: Excel inventory file missing.")
        return 1

    print("Loading inventory from '{}' (Rows {} to {})...".format(EXCEL_FILE, START_ROW, END_ROW))

    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="General Resource List", engine="openpyxl")
        df.columns = [str(column).strip().lower() for column in df.columns]
    except Exception as exc:
        print("ERROR: Failed to read Excel file: {}".format(exc))
        return 1

    start_idx = max(0, START_ROW - 2)
    end_idx = END_ROW - 1
    df = df.iloc[start_idx:end_idx]

    target_types = [equipment_type.upper() for equipment_type in EQUIPMENT_TYPES]
    target_df = df[df["equipment_type"].astype(str).str.upper().isin(target_types)]

    if target_df.empty:
        print("No servers matching criteria found.")
        return 0

    print("Found {} target server(s). Beginning configuration...\n".format(len(target_df)))

    global_has_errors = False

    for index, row in target_df.iterrows():
        print("-" * 78)
        
        required_columns = ["ilo_ip", "scope", "hostname", "ilo_hostname"]
        missing_fields = [c for c in required_columns if c not in row or pd.isna(row[c]) or str(row[c]).strip() == ""]

        if missing_fields:
            server_name = str(row.get("hostname", "Unknown"))
            print("WARNING: Skipping server '{}'. Missing: {}".format(server_name, ", ".join(missing_fields)))
            global_has_errors = True
            continue

        ip = str(row["ilo_ip"]).strip()
        scope = str(row["scope"]).strip().upper()
        
        server_name = str(row["hostname"]).strip()
        server_fqdn = str(row["ilo_hostname"]).strip()
        equipment_type = str(row["equipment_type"]).strip()

        print("Processing: {} | IP: {} | Type: {} | Scope: {}".format(server_name, ip, equipment_type, scope))

        if scope not in SCOPE_SETTINGS:
            print("  [WARNING] Scope '{}' is not defined. Skipping server.".format(scope))
            global_has_errors = True
            continue
            
        scope_data = SCOPE_SETTINGS[scope]

        if not is_reachable(ip):
            print("  [ERROR] iLO IP {} is unreachable. Skipping server.".format(ip))
            global_has_errors = True
            continue

        client = RedfishClient(ip=ip, username=ILO_LOGIN, password=ILO_PASSWORD)
        
        server_has_errors = False
        server_needs_reset = False

        try:
            if not client.login():
                print("  [ERROR] Authentication failed. Skipping server.")
                global_has_errors = True
                continue

            client.discover_resources()
            
            tasks = [
                (apply_license, (client,)),
                (apply_fencing_user, (client,)),
                (configure_ldap, (client, scope_data)),               
                (configure_ldap_certificate, (client,)),             
                (configure_server_identification, (client, server_name, server_fqdn)),
                (configure_ilo_network, (client, server_fqdn, scope_data)),
                (configure_ipmi, (client,)),
                (set_boot_order, (client,))
            ]

            for task_func, args in tasks:
                try:
                    success, needs_reset = task_func(*args)
                    if not success:
                        server_has_errors = True
                        global_has_errors = True
                    if needs_reset:
                        server_needs_reset = True
                except Exception as e:
                    print("  [ERROR] Execution of task failed: {}".format(e))
                    server_has_errors = True
                    global_has_errors = True

            if server_needs_reset:
                trigger_ilo_reset(client)

            print("\n  " + "=" * 70)
            if server_has_errors:
                print("  Configuration completed for {} with errors.".format(server_name))
            else:
                print("  Configuration completed for {} successfully.".format(server_name))
            print("  " + "=" * 70)

        except Exception as exc:
            print("\n  [CRITICAL ERROR] {}".format(exc))
            global_has_errors = True
        finally:
            client.logout()

    print("\n" + "=" * 78)
    if global_has_errors:
        print("Script execution completed with errors.")
    else:
        print("Script execution completed successfully.")
    print("=" * 78 + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())