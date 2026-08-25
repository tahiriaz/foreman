#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import subprocess
import urllib3
import requests
import openpyxl
import pandas as pd
import concurrent.futures
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
START_ROW = 1057             # Start row in Excel (1-indexed)
END_ROW = 1072               # End row in Excel (inclusive)
MAX_WORKERS = 16             # Max concurrent iLO threads

SCOPE_SETTINGS = {
    "SIL": {
            "PRIMARY_DNS": "10.130.2.11",
            "SECONDARY_DNS": "10.130.2.12",
            "DIRECTORY_SERVER": "INFCOSADU001MP.mak.iss"
        },
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

# Directory name for saving execution logs/reports
LOG_DIR_NAME = "logs"

# ============================================================================
# REDFISH SETTINGS
# ============================================================================
REDFISH_PORT = 443
REQUEST_TIMEOUT = 30

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def log(server_name, ip, message):
    """Thread-safe formatted logger."""
    print(f"[{server_name} | {ip}] {message}")

def is_reachable(ip, server_name):
    log(server_name, ip, "Pinging...")
    command = ["ping", "-n", "2", "-w", "500", str(ip)] if os.name == "nt" else ["ping", "-c", "2", "-W", "1", str(ip)]
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

def load_resource_excel_fast(filepath, sheet_name, start_row, end_row):
    """Reads Excel using openpyxl in read_only streaming mode."""
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    if sheet_name not in wb.sheetnames:
        wb.close()
        raise ValueError(f"Sheet '{sheet_name}' not found in the workbook.")
    
    ws = wb[sheet_name]
    header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
    headers = [str(c).strip().lower() if c else f"unnamed_{j}" for j, c in enumerate(header_row)]
    
    data = []
    for row in ws.iter_rows(min_row=start_row, max_row=end_row, values_only=True):
        if not any(cell is not None and str(cell).strip() != "" for cell in row):
            continue
        data.append(row)
            
    wb.close()
    return pd.DataFrame(data, columns=headers)

# ============================================================================
# REDFISH CLIENT
# ============================================================================

class RedfishClient(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.base_url = f"https://{ip}:{REDFISH_PORT}/redfish/v1"
        
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "OData-Version": "4.0",
            "Connection": "close"
        })
        
        retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        
        self.token = None
        self.manager_uri = None
        self.system_uri = None

    def login(self):
        payload = {"UserName": self.username, "Password": self.password}
        url = f"{self.base_url}/SessionService/Sessions"
        
        try:
            response = self.session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            if response.status_code in [200, 201]:
                self.token = response.headers.get("X-Auth-Token")
                if self.token:
                    self.session.headers.update({"X-Auth-Token": self.token})
                    self.session.auth = None
                return True
                
            self.session.auth = (self.username, self.password)
            response = self.session.get(f"{self.base_url}/", timeout=REQUEST_TIMEOUT)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def logout(self):
        self.session.close()

    def _request(self, method, endpoint, payload=None):
        url = f"https://{self.ip}:{REDFISH_PORT}{endpoint}" if endpoint.startswith("/redfish/v1") else f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs = {"timeout": REQUEST_TIMEOUT}
        if payload is not None: kwargs["json"] = payload
        return self.session.request(method, url, **kwargs)

    def get(self, endpoint): return self._request("GET", endpoint)
    def post(self, endpoint, payload): return self._request("POST", endpoint, payload=payload)
    def patch(self, endpoint, payload): return self._request("PATCH", endpoint, payload=payload)

    def discover_resources(self):
        data = self.get("/").json()
        managers = self.get(data.get("Managers", {}).get("@odata.id")).json()
        self.manager_uri = managers.get("Members", [])[0].get("@odata.id")

        systems = self.get(data.get("Systems", {}).get("@odata.id")).json()
        self.system_uri = systems.get("Members", [])[0].get("@odata.id")

# ============================================================================
# CONFIGURATION TASKS
# ============================================================================

def apply_license(client, log_prefix):
    endpoint = client.manager_uri.rstrip('/') + "/LicenseService/"
    response = client.get(endpoint)
    
    if response.status_code == 200:
        for member in response.json().get("Members", []):
            lic_res = client.get(member.get("@odata.id"))
            if lic_res.status_code == 200 and "Advanced" in str(lic_res.json().get("License", "")):
                log(log_prefix[0], log_prefix[1], "iLO Advanced license already installed.")
                return "SKIP", False

    log(log_prefix[0], log_prefix[1], "Applying iLO Advanced license...")
    response = client.post(endpoint, {"LicenseKey": ILO_ADVANCED_LICENSE_KEY})
    if response_is_success(response):
        time.sleep(5)
        return "OK", False
    return "FAIL", False

def apply_fencing_user(client, log_prefix):
    response = client.get("/AccountService/Accounts/")
    if response.status_code == 200:
        for member in response.json().get("Members", []):
            acc_res = client.get(member.get("@odata.id"))
            if acc_res.status_code == 200 and acc_res.json().get("UserName") == FENCE_USER_LOGIN:
                log(log_prefix[0], log_prefix[1], f"Fencing user '{FENCE_USER_LOGIN}' already exists.")
                return "SKIP", False

    log(log_prefix[0], log_prefix[1], "Creating fencing user...")
    payload = {
        "UserName": FENCE_USER_LOGIN, "Password": FENCE_USER_PASSWORD,
        "Oem": {"Hpe": {"LoginName": FENCE_USER_LOGIN, "Privileges": {"LoginPriv": True, "VirtualPowerAndResetPriv": True, "RemoteConsolePriv": False, "VirtualMediaPriv": False, "UserConfigPriv": False, "iLOConfigPriv": False}}}
    }
    return ("OK", False) if response_is_success(client.post("/AccountService/Accounts/", payload)) else ("FAIL", False)

def configure_ldap(client, scope_data, log_prefix):
    log(log_prefix[0], log_prefix[1], "Configuring Generic LDAP...")
    ldap_payload = {
        "ActiveDirectory": {"ServiceEnabled": False},
        "LDAP": {
            "ServiceEnabled": True, "ServiceAddresses": [scope_data["DIRECTORY_SERVER"]],
            "Authentication": {"AuthenticationType": "UsernameAndPassword"},
            "LDAPService": {"SearchSettings": {"BaseDistinguishedNames": [DIR_USER_CONTEXT_1, DIR_USER_CONTEXT_2, DIR_USER_CONTEXT_3, DIR_USER_CONTEXT_4]}},
            "RemoteRoleMapping": [{"LocalRole": "Administrator", "RemoteGroup": AD_GROUP_DN}]
        },
        "Oem": {"Hpe": {"DirectorySettings": {"LdapAuthenticationMode": "DefaultSchema"}}}
    }
    response = client.patch("/AccountService/", ldap_payload)
    return ("OK", check_reset_required(response)) if response_is_success(response) else ("FAIL", False)

def configure_ldap_certificate(client, log_prefix):
    if not CERT_FILE.is_file():
        log(log_prefix[0], log_prefix[1], f"Certificate file missing: {CERT_FILE}")
        return "SKIP", False

    with open(CERT_FILE, "r") as f: certificate = f.read().strip()

    cert_res = client.post("/AccountService/ExternalAccountProviders/LDAP/Certificates/", {"CertificateString": certificate, "CertificateType": "PEM"})
    if response_is_success(cert_res):
        log(log_prefix[0], log_prefix[1], "LDAP CA certificate imported (Standard).")
        return "OK", check_reset_required(cert_res)

    cert_res_oem = client.post(client.manager_uri.rstrip('/') + "/SecurityService/Actions/Oem/Hpe/HpeiLOSecurityService.ImportDirectoryCACertificate", {"Certificate": certificate})
    if response_is_success(cert_res_oem):
        log(log_prefix[0], log_prefix[1], "LDAP CA certificate imported (OEM).")
        return "OK", check_reset_required(cert_res_oem)
        
    return "FAIL", False

def configure_server_identification(client, server_name, server_fqdn, log_prefix):
    response = client.patch(client.system_uri.rstrip('/') + "/", {"HostName": server_name, "Oem": {"Hpe": {"ServerFQDN": server_fqdn}}})
    return ("OK", check_reset_required(response)) if response_is_success(response) else ("FAIL", False)

def configure_ilo_network(client, server_fqdn, scope_data, log_prefix):
    ethernet_uri = client.manager_uri.rstrip('/') + "/EthernetInterfaces/1/"
    client.patch(ethernet_uri, {"Oem": {"Hpe": {"DHCPv4": {"UseDNSServers": False, "UseDomainName": False, "UseNTPServers": False}, "DHCPv6": {"UseDNSServers": False, "UseDomainName": False, "UseNTPServers": False}}}})
    response = client.patch(ethernet_uri, {"HostName": server_fqdn.split('.')[0], "StaticNameServers": [scope_data["PRIMARY_DNS"], scope_data["SECONDARY_DNS"]], "Oem": {"Hpe": {"DomainName": ILO_DOMAIN}}})
    return ("OK", check_reset_required(response)) if response_is_success(response) else ("FAIL", False)

def configure_ipmi(client, log_prefix):
    response = client.patch(client.manager_uri.rstrip('/') + "/NetworkProtocol/", {"IPMI": {"ProtocolEnabled": True, "Port": IPMI_PORT}})
    return ("OK", check_reset_required(response)) if response_is_success(response) else ("FAIL", False)

def set_boot_order(client, log_prefix):
    response = client.patch(client.system_uri.rstrip('/') + "/", {"Boot": {"BootSourceOverrideTarget": "Pxe", "BootSourceOverrideEnabled": "Once"}})
    return ("OK", check_reset_required(response)) if response_is_success(response) else ("FAIL", False)

# ============================================================================
# PARALLEL WORKER FUNCTION
# ============================================================================

def process_server(row_dict):
    start_time = time.time()
    
    server_name = str(row_dict.get("hostname", "Unknown")).strip()
    ip = str(row_dict.get("ilo_ip", "")).strip()
    scope = str(row_dict.get("scope", "")).strip().upper()
    server_fqdn = str(row_dict.get("ilo_hostname", "")).strip()
    
    # Initialize report record dict with Hostname instead of Slot
    result = {
        "Hostname": server_name, "IP": ip, "Status": "Failed",
        "AUTH": "-", "LIC": "-", "USR": "-", "NET": "-", "IPMI": "-", 
        "ID": "-", "LDAP": "-", "CERT": "-", "BOOT": "-", "Time": 0.0
    }

    if not ip or not server_name or not scope or not server_fqdn:
        result["Status"] = "Skipped"
        return result

    if scope not in SCOPE_SETTINGS:
        result["Status"] = "Skipped"
        return result

    scope_data = SCOPE_SETTINGS[scope]
    log_prefix = (server_name, ip)

    if not is_reachable(ip, server_name):
        return result

    client = RedfishClient(ip=ip, username=ILO_LOGIN, password=ILO_PASSWORD)
    server_has_errors = False
    server_needs_reset = False

    try:
        log(*log_prefix, "Authenticating...")
        if not client.login():
            result["AUTH"] = "FAIL"
            return result
            
        result["AUTH"] = "OK"
        client.discover_resources()
        
        tasks = [
            ("LIC", apply_license, (client, log_prefix)),
            ("USR", apply_fencing_user, (client, log_prefix)),
            ("NET", configure_ilo_network, (client, server_fqdn, scope_data, log_prefix)),
            ("IPMI", configure_ipmi, (client, log_prefix)),
            ("ID", configure_server_identification, (client, server_name, server_fqdn, log_prefix)),
            ("LDAP", configure_ldap, (client, scope_data, log_prefix)),
            ("CERT", configure_ldap_certificate, (client, log_prefix)),
            ("BOOT", set_boot_order, (client, log_prefix))
        ]

        for task_name, task_func, args in tasks:
            try:
                status, needs_reset = task_func(*args)
                result[task_name] = status
                if status == "FAIL": server_has_errors = True
                if needs_reset: server_needs_reset = True
            except Exception as e:
                log(*log_prefix, f"Task {task_name} Exception: {e}")
                result[task_name] = "FAIL"
                server_has_errors = True

        if server_needs_reset:
            log(*log_prefix, "Triggering iLO Reset to finalize configuration...")
            client.post(client.manager_uri.rstrip('/') + "/Actions/Manager.Reset", {"ResetType": "ForceRestart"})

        result["Status"] = "Completed w/ Errors" if server_has_errors else "Successful"
        
    except Exception as exc:
        log(*log_prefix, f"Global Exception: {exc}")
        result["Status"] = "Failed"
    finally:
        client.logout()

    result["Time"] = time.time() - start_time
    return result

# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def main():
    t_start_global = time.time()
    
    print("\n" + "=" * 80)
    print("HPE ProLiant Gen10+ / iLO 5 Redfish Parallel Provisioner")
    print("=" * 80 + "\n")

    if not EXCEL_FILE.is_file():
        print(f"ERROR: Excel file not found at: {EXCEL_FILE}")
        return 1

    try:
        t_load_start = time.time()
        print(f"Loading inventory (Slicing Rows {START_ROW} to {END_ROW})...")
        df = load_resource_excel_fast(EXCEL_FILE, "General Resource List", START_ROW, END_ROW)
        time_excel_load = time.time() - t_load_start
    except Exception as exc:
        print(f"ERROR: Failed to read Excel slice: {exc}")
        return 1

    if df.empty or "equipment_type" not in df.columns:
        print("ERROR: No valid rows or 'equipment_type' column missing.")
        return 1
        
    target_types = [t.upper() for t in EQUIPMENT_TYPES]
    target_df = df[df["equipment_type"].astype(str).str.upper().isin(target_types)]

    if target_df.empty:
        print(f"No servers matching equipment types in specified row range.")
        return 0

    servers_to_process = target_df.to_dict('records')
    total_servers = len(servers_to_process)
    
    safe_workers = min(MAX_WORKERS, total_servers)
    final_report = []
    
    t_redfish_start = time.time()
    print(f"Found {total_servers} matching server(s). Starting parallel Redfish phase ({safe_workers} workers)...\n")
    
    # Multithreaded Execution Pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=safe_workers) as executor:
        futures = {executor.submit(process_server, srv): srv for srv in servers_to_process}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            final_report.append(res)
            
    time_redfish_phase = time.time() - t_redfish_start

    # ========================================================================
    # FINAL REPORT GENERATION & METRICS
    # ========================================================================
    t_report_start = time.time()
    
    # Sort alphabetically by Hostname
    sorted_report = sorted(final_report, key=lambda x: x["Hostname"])
    
    successful = sum(1 for x in final_report if x["Status"] == "Successful")
    skipped = sum(1 for x in final_report if x["Status"] == "Skipped")
    failed = total_servers - successful - skipped

    print("\nFINAL EXECUTION REPORT:")
    print("=" * 145)
    print(f"{'HOSTNAME':<18} | {'iLO IP':<15} | {'OVERALL STATUS':<15} | AUTH | LIC  | USR  | NET  | IPMI | ID   | LDAP | CERT | BOOT | Time (s)")
    print("-" * 145)
    
    for srv in sorted_report:
        print(f"{srv['Hostname']:<18} | {srv['IP']:<15} | {srv['Status']:<15} | {srv['AUTH']:<4} | {srv['LIC']:<4} | {srv['USR']:<4} | {srv['NET']:<4} | {srv['IPMI']:<4} | {srv['ID']:<4} | {srv['LDAP']:<4} | {srv['CERT']:<4} | {srv['BOOT']:<4} | {srv['Time']:>8.2f}")

    print("\n")
    print(f"TOTAL FOUND: {total_servers} | SUCCESSFUL: {successful} | FAILED: {failed} | SKIPPED: {skipped}")
    print("=" * 145 + "\n")
    
    time_report_phase = time.time() - t_report_start
    total_execution_time = time.time() - t_start_global

    # Print Performance Summary
    print("=================================================================")
    print("PERFORMANCE SUMMARY")
    print("=================================================================")
    print(f"Excel load/parse              :   {time_excel_load:>7.2f} sec")
    print(f"Parallel Redfish phase        :   {time_redfish_phase:>7.2f} sec")
    print(f"Final report                  :   {time_report_phase:>7.2f} sec")
    print("-" * 65)
    print(f"TOTAL EXECUTION TIME          :   {total_execution_time:>7.2f} sec")
    print("=================================================================\n")
    
    print("Concurrency used:")
    print(f"  Redfish sessions: {total_servers}")
    print(f"  Configured REDFISH_CONCURRENT_SESSIONS = {safe_workers}\n")

    # CSV Audit File Generation
    if final_report:
        log_dir = BASE_DIR / LOG_DIR_NAME
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        report_filename = f"ILO_RM_Report_{timestamp}.csv"
        report_path = log_dir / report_filename
        
        # Dump the exact dictionary layout into the CSV
        pd.DataFrame(sorted_report).to_csv(report_path, index=False)
        print(f"Audit log saved to: {report_path}\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())