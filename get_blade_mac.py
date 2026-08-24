import os
import re
import warnings

# ==========================================
# Suppress Deprecation Warnings
# ==========================================
# These must come BEFORE importing paramiko to successfully hide the cryptography warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Python 3.6 is no longer supported.*")
warnings.filterwarnings("ignore", module="cryptography")
warnings.filterwarnings("ignore", module="paramiko")

import paramiko
from openpyxl import load_workbook
import win32com.client as win32  # Added for formula recalculation

# ==========================================
# Global Configuration
# ==========================================
USERNAME = "Administrator"
PASSWORD = "Siljeddah15"
# ==========================================

def connect_to_oa(primary_ip, secondary_ip, user, pwd):
    """Attempts to connect to the Primary OA IP, falls back to Secondary if needed."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ips_to_try = [ip for ip in (primary_ip, secondary_ip) if ip]
    
    if not ips_to_try:
        print("Error: No OA IPs provided.")
        return None
        
    for ip in ips_to_try:
        print(f"\nAttempting connection to OA at {ip}...")
        try:
            ssh.connect(
                hostname=ip, 
                username=user, 
                password=pwd, 
                look_for_keys=False, 
                allow_agent=False,
                timeout=10
            )
            print(f"Successfully connected to OA ({ip}).")
            return ssh
        except Exception as e:
            print(f"Failed to connect to {ip}: {e}")
            
    print("Error: Could not connect to any OA IPs.")
    return None

def get_blade_details(ssh, bay):
    """Retrieves Serial Number and MAC addresses for a specific blade bay via an active SSH session."""
    # Initialize with empty strings so "MAC not found" isn't written to Excel
    macs = [""] * 6
    serial_number = "Serial Number not found"
    
    try:
        # 1. Get Serial Number
        cmd_info = f"show server info {bay}"
        stdin, stdout, stderr = ssh.exec_command(cmd_info)
        info_output = stdout.read().decode('utf-8')
        
        sn_match = re.search(r'Serial Number:\s*([A-Za-z0-9\-]+)', info_output, re.IGNORECASE)
        if sn_match:
            serial_number = sn_match.group(1).strip()

        # 2. Get Port Map for MAC addresses
        cmd_port = f"show server port map {bay}"
        stdin, stdout, stderr = ssh.exec_command(cmd_port)
        port_output = stdout.read().decode('utf-8')
        
        mac_pattern = re.compile(r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}')
        
        flb_macs = []
        other_macs = []
        current_section = "other"
        
        for line in port_output.splitlines():
            upper_line = line.upper()
            if 'LOM' in upper_line or 'FLB' in upper_line:
                current_section = "flb"
            elif 'MEZZ' in upper_line:
                current_section = "other"
                
            found_macs = mac_pattern.findall(line)
            for mac in found_macs:
                clean_mac = mac.replace('-', ':').upper()
                if current_section == "flb":
                    if clean_mac not in flb_macs:
                        flb_macs.append(clean_mac)
                else:
                    if clean_mac not in other_macs:
                        other_macs.append(clean_mac)
                        
        combined_macs = flb_macs + [m for m in other_macs if m not in flb_macs]
        
        # Assign found MACs to the 6 slots
        for i in range(min(len(combined_macs), 6)):
            macs[i] = combined_macs[i]

    except Exception as e:
        print(f"Error executing commands for bay {bay}: {e}")
        
    return serial_number, macs

def refresh_excel_formulas(file_path):
    """Uses the native Excel application in the background to rebuild formula caches."""
    print("Commanding Excel to recalculate formulas in the background...")
    try:
        # Convert to absolute path (required by COM)
        abs_path = os.path.abspath(file_path)
        excel = win32.DispatchEx("Excel.Application")
        excel.Visible = False       # Keep Excel hidden
        excel.DisplayAlerts = False # Suppress popups

        # Open, calculate, save, and close
        wb = excel.Workbooks.Open(abs_path)
        wb.Save()
        wb.Close()
        excel.Quit()
        print("Formula cache successfully rebuilt!")
    except Exception as e:
        print(f"WARNING: Could not trigger Excel to rebuild formulas: {e}")

def main():
    # Make input case-insensitive to avoid typo errors
    enclosure_name = input("Enter the Enclosure Name: ").strip().upper()
    
    # Locate the Excel file relative to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, 'Templates', 'Resource List-v7.6.xlsx')
    
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return

    print(f"\nLoading Excel file (Reading Data Mode)...")
    wb_read = load_workbook(excel_path, data_only=True)
    
    print(f"Loading Excel file (Writing Formula Mode)...")
    wb_write = load_workbook(excel_path)
    
    sheet_name = "General Resource List"
    if sheet_name not in wb_read.sheetnames:
        print(f"Error: Sheet '{sheet_name}' not found in the workbook.")
        return
        
    ws_read = wb_read[sheet_name]
    ws_write = wb_write[sheet_name]

    # Map headers to column indices
    headers = {str(cell.value).strip(): idx for idx, cell in enumerate(ws_read[1], 1) if cell.value}
    
    required_cols = [
        'equipment_physical_name', 'enclosure_physical_name', 'equipment_type', 
        'enclosure_slot', 'ilo_ip', 'serial_no', 
        'nic0_mac', 'nic1_mac', 'nic2_mac', 'nic3_mac', 'nic4_mac', 'nic5_mac'
    ]
    
    missing_cols = [col for col in required_cols if col not in headers]
    if missing_cols:
        print(f"Error: The following required columns are missing in the Excel sheet: {', '.join(missing_cols)}")
        return

    primary_oa_ip = None
    secondary_oa_ip = None
    blade_rows = []

    print("\nScanning rows...")
    
    for row in range(2, ws_read.max_row + 1):
        # We need to robustly check if the row matches the enclosure name.
        # Since it's a formula, we check the evaluated data cell, and as a fallback, 
        # we check the equipment_physical_name column (since your formula derives the name from there).
        enc_val = ws_read.cell(row=row, column=headers['enclosure_physical_name']).value
        eq_phys_val = ws_read.cell(row=row, column=headers['equipment_physical_name']).value
        
        enc_str = str(enc_val).strip().upper() if enc_val else ""
        eq_phys_str = str(eq_phys_val).strip().upper() if eq_phys_val else ""
        
        is_match = False
        if enc_str == enclosure_name:
            is_match = True
        elif len(enclosure_name) >= 14 and eq_phys_str.startswith(enclosure_name[:14]):
            is_match = True

        if is_match:
            eq_type = str(ws_read.cell(row=row, column=headers['equipment_type']).value or "").strip().upper()
            raw_slot = ws_read.cell(row=row, column=headers['enclosure_slot']).value
            
            # Safely convert slot to an integer (handles "01" and floats like 1.0)
            try:
                slot_num = int(float(str(raw_slot).strip()))
            except (ValueError, TypeError):
                slot_num = None

            # Check if this is the OA
            if "ENCLOSURE OA" in eq_type:
                ip_val = ws_read.cell(row=row, column=headers['ilo_ip']).value
                if ip_val:
                    if slot_num == 1:
                        primary_oa_ip = str(ip_val).strip()
                    elif slot_num == 2:
                        secondary_oa_ip = str(ip_val).strip()
            
            # Check if this is a Blade Server
            elif "BLADE SERVER" in eq_type:
                blade_rows.append({
                    'row_idx': row,
                    'slot': slot_num,
                    'eq_type': eq_type
                })

    if not primary_oa_ip and not secondary_oa_ip:
        print(f"Error: Could not find OA IPs for Enclosure '{enclosure_name}'.")
        return
        
    if not blade_rows:
        print(f"No Blade Servers found for Enclosure '{enclosure_name}'.")
        return

    print(f"Found Primary OA: {primary_oa_ip} | Secondary OA: {secondary_oa_ip}")
    print(f"Found {len(blade_rows)} Blade Server(s) in this enclosure.")

    # Connect to the OA
    ssh = connect_to_oa(primary_oa_ip, secondary_oa_ip, USERNAME, PASSWORD)
    if not ssh:
        return

    # Process each blade
    try:
        for blade in blade_rows:
            row_idx = blade['row_idx']
            bay_num = blade['slot']
            eq_type = blade['eq_type']
            
            print(f"\n--- Processing Row {row_idx}: {eq_type} ---")
            
            if bay_num is None:
                print(f"WARNING: Skipping blade at row {row_idx}. Missing or invalid enclosure_slot.")
                continue

            print(f"Extracting details for Bay {bay_num}...")
            serial_no, macs = get_blade_details(ssh, bay_num)
            
            # Write to the Formula-preserved workbook (wb_write)
            ws_write.cell(row=row_idx, column=headers['serial_no']).value = serial_no
            ws_write.cell(row=row_idx, column=headers['nic0_mac']).value = macs[0]
            ws_write.cell(row=row_idx, column=headers['nic1_mac']).value = macs[1]
            ws_write.cell(row=row_idx, column=headers['nic2_mac']).value = macs[2]
            ws_write.cell(row=row_idx, column=headers['nic3_mac']).value = macs[3]
            ws_write.cell(row=row_idx, column=headers['nic4_mac']).value = macs[4]
            ws_write.cell(row=row_idx, column=headers['nic5_mac']).value = macs[5]
            
            # Display results and warnings for missing MACs
            print(f"  Serial Number : {serial_no}")
            for i, mac in enumerate(macs, 1):
                if not mac:
                    print(f"  mac{i}          : [MISSING]")
                    print(f"  -> WARNING: mac{i} was not found on the server.")
                else:
                    print(f"  mac{i}          : {mac}")

        # Save the updated Excel file
        print(f"\nSaving updates to {excel_path}...")
        wb_write.save(excel_path)
        print("Excel file successfully updated!")
        
        # Trigger the formula recalculation
        refresh_excel_formulas(excel_path)
        
    finally:
        ssh.close()
        print("SSH connection closed.")

if __name__ == "__main__":
    main()