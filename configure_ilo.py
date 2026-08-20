#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import time
from pathlib import Path
import paramiko
import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined

# ============================================================================
# OA & iLO CREDENTIALS
# ============================================================================

OA_USERNAME = "Administrator"
OA_PASSWORD = "Siljeddah15"

ILO_LOGIN = "admin"
ILO_PASSWORD = "password"

# Replace with your 25-character iLO Advanced License Key
ILO_ADVANCED_LICENSE_KEY = "35SCR-RYLML-CBK7N-TD3B9-GGBW2"

FENCE_USER_NAME = "Pacemaker Fence"
FENCE_USER_LOGIN = "hpilofence"
FENCE_USER_PASSWORD = "Th@les01"

IPMI_PORT = "623"
ILO_DOMAIN = "mak.iss"

DIR_USER_CONTEXT_1 = "OU=IT,OU=ISS,DC=mak,DC=iss"
DIR_USER_CONTEXT_2 = "CN=Users,DC=mak,DC=iss"
DIR_USER_CONTEXT_3 = "CN=Builtin,DC=mak,DC=iss"
DIR_USER_CONTEXT_4 = "@mak.iss"

# ============================================================================
# SCOPE MAPPINGS (MTR vs RTR)
# ============================================================================

SCOPE_SETTINGS = {
    "MTR": {
        "PRIMARY_DNS": "10.130.2.11",
        "SECONDARY_DNS": "10.130.2.12",
        "DIRECTORY_SERVER": "INFCOSADU001MP.mak.iss"
    },
    "RTR": {
        "PRIMARY_DNS": "10.130.3.11", 
        "SECONDARY_DNS": "10.130.3.12",
        "DIRECTORY_SERVER": "INFCOSADU002MP.mak.iss"
    }
}

# ============================================================================
# SETTINGS & PATHS
# ============================================================================

DEBUG_MODE = 0

SSH_PORT = 22
SSH_CONNECT_TIMEOUT = 15
COMMAND_TIMEOUT = 180
COMMAND_QUIET_TIME = 15.0 

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "Templates"
TEMPLATE_FILE = "ilo_config.xml.j2"
EXCEL_FILE = TEMPLATE_DIR / "Resource List-v7.6.xlsx"

# ============================================================================
# CORE LOGIC
# ============================================================================

def create_jinja_environment():
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )

def render_template(add_user, apply_ipmi_config, apply_license, scope_data, server_name, server_fqdn):
    env = create_jinja_environment()
    template = env.get_template(TEMPLATE_FILE)
    return template.render(
        apply_license=apply_license,
        ilo_license_key=ILO_ADVANCED_LICENSE_KEY,
        add_user=add_user,
        apply_ipmi_config=apply_ipmi_config,
        ilo_login=ILO_LOGIN, ilo_password=ILO_PASSWORD,
        fence_user_name=FENCE_USER_NAME, fence_user_login=FENCE_USER_LOGIN,
        fence_user_password=FENCE_USER_PASSWORD,
        ipmi_port=IPMI_PORT,
        server_name=server_name,
        server_fqdn=server_fqdn,
        ilo_domain=ILO_DOMAIN, 
        primary_dns=scope_data["PRIMARY_DNS"],
        secondary_dns=scope_data["SECONDARY_DNS"], 
        directory_server=scope_data["DIRECTORY_SERVER"],
        dir_user_context_1=DIR_USER_CONTEXT_1,
        dir_user_context_2=DIR_USER_CONTEXT_2,
        dir_user_context_3=DIR_USER_CONTEXT_3,
        dir_user_context_4=DIR_USER_CONTEXT_4,
    )

class OAConnection(object):
    def __init__(self, username, password, port=22):
        self.hostname = None
        self.username = username
        self.password = password
        self.port = port
        self.client = None
        self.channel = None

    def connect(self, hostname):
        self.hostname = hostname
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.hostname, port=self.port,
            username=self.username, password=self.password,
            timeout=SSH_CONNECT_TIMEOUT, look_for_keys=False, allow_agent=False,
        )
        self.channel = self.client.invoke_shell()
        time.sleep(1)
        self._drain_channel()

    def close(self):
        if self.channel:
            try: self.channel.close()
            except Exception: pass
        if self.client:
            try: self.client.close()
            except Exception: pass

    def _drain_channel(self):
        if not self.channel: return ""
        output = ""
        while self.channel.recv_ready():
            data = self.channel.recv(65535)
            if not data: break
            output += data.decode("utf-8", errors="replace")
        return output

    def read_command_output(self, timeout=COMMAND_TIMEOUT):
        output = ""
        deadline = time.monotonic() + timeout
        quiet_since = None

        while time.monotonic() < deadline:
            if self.channel.recv_ready():
                data = self.channel.recv(65535)
                if not data: break
                output += data.decode("utf-8", errors="replace")
                quiet_since = None
            else:
                if quiet_since is None:
                    quiet_since = time.monotonic()
                elif time.monotonic() - quiet_since >= COMMAND_QUIET_TIME:
                    break
                time.sleep(0.1)
        else:
            raise TimeoutError("Timed out waiting for OA command output.")
        return output

    def execute_hponcfg(self, bay_number, ribcl, end_marker="ILO_RIBCL_EOF"):
        self._drain_channel()
        command = "HPONCFG {0} << {1}\n{2}\n{1}\n".format(
            bay_number, end_marker, ribcl.rstrip()
        )
        for line in command.splitlines():
            self.channel.send(line + "\n")
            time.sleep(0.05)
        return self.read_command_output()

def check_fence_user(oa, bay_number):
    print(f"  -> Checking if user '{FENCE_USER_LOGIN}' exists...")
    ribcl = '<RIBCL VERSION="2.0">\n<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n<USER_INFO MODE="read">\n<GET_USER USER_LOGIN="{2}"/>\n</USER_INFO>\n</LOGIN>\n</RIBCL>'.format(
        ILO_LOGIN, ILO_PASSWORD, FENCE_USER_LOGIN
    )
    output = oa.execute_hponcfg(bay_number=bay_number, ribcl=ribcl, end_marker="ILO_USER_CHECK_EOF")
    
    statuses = re.findall(r'<RESPONSE\s+STATUS=["\']([^"\']+)["\']', output, re.IGNORECASE)
    
    if "0x000A" in statuses:
        return False
    if "0x0000" in statuses:
        return True
    return False

def check_ipmi_settings(oa, bay_number):
    print(f"  -> Checking current IPMI settings...")
    ribcl = '<RIBCL VERSION="2.0">\n<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n<RIB_INFO MODE="read">\n<GET_GLOBAL_SETTINGS/>\n</RIB_INFO>\n</LOGIN>\n</RIBCL>'.format(
        ILO_LOGIN, ILO_PASSWORD
    )
    output = oa.execute_hponcfg(bay_number=bay_number, ribcl=ribcl, end_marker="ILO_IPMI_CHECK_EOF")
    
    port_match = re.search(r'IPMI_DCMI_OVER_LAN_PORT\s*VALUE\s*=\s*["\'](\d+)["\']', output, re.IGNORECASE)
    enabled_match = re.search(r'IPMI_DCMI_OVER_LAN_ENABLED\s*VALUE\s*=\s*["\']([Yy])["\']', output, re.IGNORECASE)
    
    is_enabled = bool(enabled_match)
    port_is_target = bool(port_match and port_match.group(1) == str(IPMI_PORT))
    
    if is_enabled and port_is_target:
        print(f"  -> IPMI is already ENABLED on port {IPMI_PORT}. Skipping IPMI block.")
        return False
    else:
        print("  -> IPMI needs configuration. Queuing global settings update.")
        return True

def check_ilo_license(oa, bay_number):
    print(f"  -> Checking current iLO License status...")
    ribcl = '<RIBCL VERSION="2.0">\n<LOGIN USER_LOGIN="{0}" PASSWORD="{1}">\n<RIB_INFO MODE="read">\n<GET_ALL_LICENSES/>\n</RIB_INFO>\n</LOGIN>\n</RIBCL>'.format(
        ILO_LOGIN, ILO_PASSWORD
    )
    output = oa.execute_hponcfg(bay_number=bay_number, ribcl=ribcl, end_marker="ILO_LICENSE_CHECK_EOF")
    
    match = re.search(r'LICENSE_TYPE\s*VALUE\s*=\s*["\']([^"\']+)["\']', output, re.IGNORECASE)
    
    if match:
        license_type = match.group(1)
        print(f"  -> Detected License: {license_type}")
        if "Advanced" in license_type:
            print("  -> iLO Advanced features are already enabled. Skipping license application.")
            return False
            
    print("  -> iLO Advanced features NOT found or undetermined. Queuing license activation.")
    return True

def validate_hponcfg_result(output):
    if "END RIBCL RESULTS" not in output:
        print("\n  [ERROR] OA did not finish sending the RIBCL results. The SSH read timed out.")
        return False

    responses = re.findall(r'<RESPONSE\s+STATUS=["\']([^"\']+)["\']\s+MESSAGE=[\'"]([^\'"]+)[\'"]', output, re.IGNORECASE)
    
    has_error = False
    for status, message in responses:
        if status != "0x0000":
            print(f"  [ERROR] iLO rejected configuration: STATUS={status} | MESSAGE='{message}'")
            has_error = True
            
    if has_error:
        print("  [FAILURE] iLO rejected one or more configuration blocks.")
        return False
    
    print("  [SUCCESS] Configuration applied to Bay.")
    return True

# ============================================================================
# MAIN
# ============================================================================

def main():
    if not EXCEL_FILE.is_file():
        print(f"ERROR: Excel inventory file missing: {EXCEL_FILE}", file=sys.stderr)
        return 1

    enclosure_input = input("Enter Enclosure Name: ").strip()
    if not enclosure_input:
        print("ERROR: Enclosure name cannot be empty.")
        return 1

    print(f"\nLoading inventory from '{EXCEL_FILE}'...")
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="General Resource List", engine="openpyxl")
        df.columns = [str(c).strip().lower() for c in df.columns]
    except Exception as e:
        print(f"ERROR: Failed to read Excel file: {e}")
        return 1

    enc_df = df[df['enclosure_physical_name'] == enclosure_input]
    if enc_df.empty:
        print(f"ERROR: Enclosure '{enclosure_input}' not found in inventory.")
        return 1

    oa_df = enc_df[enc_df['equipment_type'] == 'Enclosure OA']
    
    primary_oa_ip = None
    secondary_oa_ip = None
    
    for _, row in oa_df.iterrows():
        slot = row.get('enclosure_slot')
        ip = row.get('ilo_ip')
        if pd.notna(slot) and pd.notna(ip):
            if int(float(slot)) == 1:
                primary_oa_ip = str(ip).strip()
            elif int(float(slot)) == 2:
                secondary_oa_ip = str(ip).strip()

    if not primary_oa_ip and not secondary_oa_ip:
        print(f"ERROR: No OA IP addresses found for enclosure '{enclosure_input}'.")
        return 1

    oa = OAConnection(username=OA_USERNAME, password=OA_PASSWORD, port=SSH_PORT)
    connected = False
    
    for ip in [primary_oa_ip, secondary_oa_ip]:
        if not ip:
            continue
        print(f"\nAttempting to connect to OA at {ip}...")
        try:
            oa.connect(hostname=ip)
            connected = True
            print(f"SUCCESS: Connected to OA at {ip}.")
            break
        except Exception as e:
            print(f"WARNING: Failed to connect to {ip}: {e}")

    if not connected:
        print("\nERROR: Could not connect to any OA. Exiting.")
        return 1

    blade_df = enc_df[enc_df['equipment_type'].astype(str).str.contains('Blade Server', na=False, case=False)]
    
    if blade_df.empty:
        print(f"\nNo Blade Servers found for enclosure '{enclosure_input}'. Exiting.")
        oa.close()
        return 0

    print(f"\nFound {len(blade_df)} Blade Server(s) in enclosure '{enclosure_input}'. Beginning configuration...\n")

    try:
        for idx, row in blade_df.iterrows():
            print("-" * 78)
            
            missing_fields = []
            required_cols = ['enclosure_slot', 'scope', 'hostname', 'ilo_hostname']
            
            for col in required_cols:
                if col not in row or pd.isna(row[col]) or str(row[col]).strip() == "":
                    missing_fields.append(col)

            try:
                bay_number = int(float(row['enclosure_slot']))
            except (ValueError, TypeError):
                bay_number = "Unknown"
                if 'enclosure_slot' not in missing_fields:
                    missing_fields.append('enclosure_slot (invalid number)')

            if missing_fields:
                print(f"WARNING: Skipping Blade in Bay {bay_number}. Missing required fields: {', '.join(missing_fields)}")
                continue

            scope = str(row['scope']).strip().upper()
            server_name = str(row['hostname']).strip()
            server_fqdn = str(row['ilo_hostname']).strip()

            if scope not in SCOPE_SETTINGS:
                print(f"WARNING: Skipping Bay {bay_number}. Scope '{scope}' is not defined in SCOPE_SETTINGS.")
                continue

            print(f"Configuring Bay {bay_number} | Server: {server_name} | Scope: {scope}")
            scope_data = SCOPE_SETTINGS[scope]

            # 1. Check License
            apply_license = check_ilo_license(oa, bay_number)

            # 2. Check User
            user_exists = check_fence_user(oa, bay_number)
            if user_exists:
                print(f"  -> User '{FENCE_USER_LOGIN}' exists. Skipping creation.")
            else:
                print(f"  -> User '{FENCE_USER_LOGIN}' missing. Queuing creation.")

            # 3. Check IPMI
            apply_ipmi = check_ipmi_settings(oa, bay_number)

            # 4. Render and Push
            ribcl = render_template(
                add_user=not user_exists, 
                apply_ipmi_config=apply_ipmi,
                apply_license=apply_license,
                scope_data=scope_data,
                server_name=server_name,
                server_fqdn=server_fqdn
            )
            
            print("  -> Pushing RIBCL configuration (this will take 10-20 seconds)...")
            result = oa.execute_hponcfg(bay_number=bay_number, ribcl=ribcl)

            if DEBUG_MODE == 1:
                print("\n" + "=" * 78)
                print(f"DEBUG: RAW RIBCL RESULTS (BAY {bay_number})")
                print("=" * 78)
                print(result)
                print("=" * 78 + "\n")

            validate_hponcfg_result(result)

    except Exception as exc:
        print(f"\nERROR during execution: {exc}", file=sys.stderr)
    finally:
        oa.close()
        print("\n" + "=" * 78)
        print("Script execution completed.")
        print("=" * 78)

if __name__ == "__main__":
    sys.exit(main())