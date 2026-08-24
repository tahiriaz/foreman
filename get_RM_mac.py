import os
import re
import warnings
import platform
import subprocess
import requests
from openpyxl import load_workbook

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Suppress Python 3.6 cryptography warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # Suppress self-signed cert warnings for iLO

# ==========================================
# Global Configuration Variables
# ==========================================
USERNAME = "Administrator"
PASSWORD = "Th@les01"

# Directory and File Settings
EXCEL_DIR = "Templates"
EXCEL_FILE = "Resource List-v7.6.xlsx"
SHEET_NAME = "General Resource List"

# Processing Scope
START_ROW = 2
END_ROW = 500  # Adjust as needed, or set to None to process to the end of the sheet

# Target Equipment Types and Expected MACs (Case-Insensitive)
# Dictionary format: {"EQUIPMENT TYPE NAME": expected_mac_count}
TARGET_EQUIPMENT = {
    "ESXi": 4,
    "NVR": 4,
    "VCA": 4
}

# Required columns for a row to be processed
REQUIRED_COLUMNS = [
    'ilo_ip', 'equipment_type', 'serial_no',
    'nic0_mac', 'nic1_mac', 'nic2_mac', 'nic3_mac', 'nic4_mac', 'nic5_mac'
]

# Ping Settings
PING_COUNT = 2
PING_TIMEOUT_MS = 300

# Debug Toggle
DEBUG = False
# ==========================================

def print_debug(msg):
    """Helper function to print debug messages if debugging is enabled."""
    if DEBUG:
        print(f"[DEBUG] {msg}")

def ping_host(ip_address, count=PING_COUNT, timeout_ms=PING_TIMEOUT_MS):
    """Pings a host to check if it's alive before attempting an API connection."""
    param_count = '-n' if platform.system().lower() == 'windows' else '-c'
    param_timeout = '-w' if platform.system().lower() == 'windows' else '-W'
    
    # Note: Linux ping timeout is usually in seconds, Windows in ms. 
    # Adjusting for Linux if necessary (converting ms to seconds, min 1)
    if platform.system().lower() != 'windows':
        timeout_val = str(max(1, int(timeout_ms / 1000)))
    else:
        timeout_val = str(timeout_ms)

    command = ['ping', param_count, str(count), param_timeout, timeout_val, ip_address]
    
    print_debug(f"Executing ping command: {' '.join(command)}")
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output.returncode == 0
    except Exception as e:
        print_debug(f"Ping execution failed: {e}")
        return False

def get_redfish_details(ilo_ip, user, pwd):
    """Connects to the iLO Redfish API to get Serial Number and NIC MAC addresses."""
    serial_number = "Serial Number not found"
    macs = []
    
    base_url = f"https://{ilo_ip}"
    auth = (user, pwd)
    
    try:
        # 1. Get Serial Number from the System chassis
        sys_url = f"{base_url}/redfish/v1/Systems/1"
        print_debug(f"Requesting System Info: {sys_url}")
        sys_resp = requests.get(sys_url, auth=auth, verify=False, timeout=10)
        
        if sys_resp.status_code == 200:
            sys_data = sys_resp.json()
            serial_number = sys_data.get('SerialNumber', serial_number).strip()
        else:
            print_debug(f"Failed to get System Info. HTTP {sys_resp.status_code}")

        # 2. Get MAC Addresses from EthernetInterfaces
        # Redfish stores host NICs in Systems/1/EthernetInterfaces (which excludes the iLO management interface)
        eth_url = f"{base_url}/redfish/v1/Systems/1/EthernetInterfaces"
        print_debug(f"Requesting Ethernet Interfaces: {eth_url}")
        eth_resp = requests.get(eth_url, auth=auth, verify=False, timeout=10)
        
        if eth_resp.status_code == 200:
            eth_data = eth_resp.json()
            members = eth_data.get('Members', [])
            
            for member in members:
                ifc_uri = member.get('@odata.id')
                if ifc_uri:
                    ifc_resp = requests.get(f"{base_url}{ifc_uri}", auth=auth, verify=False, timeout=10)
                    if ifc_resp.status_code == 200:
                        mac = ifc_resp.json().get('MACAddress')
                        if mac:
                            # Standardize MAC format
                            clean_mac = mac.replace('-', ':').upper()
                            if clean_mac not in macs:
                                macs.append(clean_mac)
        else:
            print_debug(f"Failed to get Ethernet Interfaces. HTTP {eth_resp.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"  -> Connection error while communicating with Redfish API: {e}")

    # Ensure we return a list of exactly 6 elements
    padded_macs = (macs + ["MAC not found"] * 6)[:6]
    return serial_number, padded_macs

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, EXCEL_DIR, EXCEL_FILE)
    
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return

    print(f"\nLoading Excel file (Reading Data Mode)...")
    # Utilizing data_only=True to evaluate formulas (mimics engine="openpyxl" behavior in Pandas)
    wb_read = load_workbook(excel_path, data_only=True)
    
    print(f"Loading Excel file (Writing Formula Mode)...")
    wb_write = load_workbook(excel_path)
    
    if SHEET_NAME not in wb_read.sheetnames:
        print(f"Error: Sheet '{SHEET_NAME}' not found in the workbook.")
        return
        
    ws_read = wb_read[SHEET_NAME]
    ws_write = wb_write[SHEET_NAME]

    # Map headers to column indices
    headers = {str(cell.value).strip(): idx for idx, cell in enumerate(ws_read[1], 1) if cell.value}
    
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in headers]
    if missing_cols:
        print(f"Error: Required columns missing in the Excel sheet: {', '.join(missing_cols)}")
        return

    # Scan for target servers
    servers_to_process = []
    
    max_row = END_ROW if END_ROW else ws_read.max_row
    max_row = min(max_row, ws_read.max_row)

    print("\nScanning rows for Target Equipment...")
    for row in range(START_ROW, max_row + 1):
        raw_eq = ws_read.cell(row=row, column=headers['equipment_type']).value
        eq_type = str(raw_eq or "").strip().upper()
        
        # Check against target dictionary keys
        if eq_type in TARGET_EQUIPMENT:
            # Get the evaluated IP (handles formula outputs)
            ilo_ip = str(ws_read.cell(row=row, column=headers['ilo_ip']).value or "").strip()
            
            servers_to_process.append({
                'row_idx': row,
                'eq_type': eq_type,
                'ilo_ip': ilo_ip,
                'expected_macs': TARGET_EQUIPMENT[eq_type]
            })

    print(f"\nFound {len(servers_to_process)} rackmount server(s) matching criteria.\n" + "="*50)

    # Process each server
    for server in servers_to_process:
        row_idx = server['row_idx']
        eq_type = server['eq_type']
        ilo_ip = server['ilo_ip']
        expected_macs = server['expected_macs']
        
        print(f"\n--- Processing Row {row_idx}: {eq_type} (iLO IP: {ilo_ip}) ---")
        
        if not ilo_ip or ilo_ip.lower() == "none":
            print(f"WARNING: Skipping row {row_idx}. iLO IP is missing or invalid.")
            continue
            
        print(f"Pinging {ilo_ip} to verify reachability...")
        if not ping_host(ilo_ip):
            print(f"WARNING: Host {ilo_ip} is unreachable via ping (Timeout: {PING_TIMEOUT_MS}ms). Skipping.")
            continue
            
        print(f"Connecting to Redfish API on {ilo_ip}...")
        serial_no, macs = get_redfish_details(ilo_ip, USERNAME, PASSWORD)
        
        # Write to Formula-preserved workbook
        ws_write.cell(row=row_idx, column=headers['serial_no']).value = serial_no
        ws_write.cell(row=row_idx, column=headers['nic0_mac']).value = macs[0]
        ws_write.cell(row=row_idx, column=headers['nic1_mac']).value = macs[1]
        ws_write.cell(row=row_idx, column=headers['nic2_mac']).value = macs[2]
        ws_write.cell(row=row_idx, column=headers['nic3_mac']).value = macs[3]
        ws_write.cell(row=row_idx, column=headers['nic4_mac']).value = macs[4]
        ws_write.cell(row=row_idx, column=headers['nic5_mac']).value = macs[5]
        
        # Display Results based on EXPECTED number of MACs
        print(f"  Serial Number : {serial_no}")
        found_mac_count = 0
        
        for i in range(expected_macs):
            mac_val = macs[i]
            print(f"  mac{i+1}          : {mac_val}")
            
            if mac_val == "MAC not found":
                print(f"  -> WARNING: Expected mac{i+1} was not found on this server.")
            else:
                found_mac_count += 1
                
        if found_mac_count < expected_macs:
            print(f"  -> OVERALL WARNING: Expected {expected_macs} MACs, but only found {found_mac_count}.")

    # Save Excel Changes
    print(f"\nSaving updates to {excel_path}...")
    try:
        wb_write.save(excel_path)
        print("Excel file successfully updated!")
    except PermissionError:
        print(f"ERROR: Cannot save Excel file. Please ensure '{EXCEL_FILE}' is not open in another program.")

if __name__ == "__main__":
    main()