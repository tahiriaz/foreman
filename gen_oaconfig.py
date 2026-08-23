import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# ==========================================
# 1. Variables Definition
# ==========================================

# Scope-specific network variables mapping
scope_vars = {
    "SIL": {
            "gateway": "10.101.18.1",
            "mask": "255.255.254.0",
            "dns1": "10.130.2.11",
            "dns2": "10.130.2.12",
            "ntp1": "10.101.18.1",
            "ntp2": "10.130.2.11",
            "domain_controller": "INFCOSADU001MP.mak.iss"
        },
    "MTR": {
        "gateway": "10.101.18.1",
        "mask": "255.255.254.0",
        "dns1": "10.130.2.11",
        "dns2": "10.130.2.12",
        "ntp1": "10.101.18.1",
        "ntp2": "10.130.2.11",
        "domain_controller": "INFCOSADU001MP.mak.iss"
    },
    "RTR": {
        "gateway": "10.102.18.1",              # Fill with RTR specific gateway
        "mask": "255.255.254.0",                 # Fill with RTR specific mask
        "dns1": "10.130.4.11",                 # Fill with RTR specific DNS1
        "dns2": "10.130.4.12",                 # Fill with RTR specific DNS2
        "ntp1": "10.102.18.1",                 # Fill with RTR specific NTP1
        "ntp2": "10.130.2.11",                 # Fill with RTR specific NTP2
        "domain_controller": "INFCOSADU001RP.mak.iss"     # Fill with RTR specific DC
    }
}

# Standard global variables
domain = "mak.iss"
ilo_admin_group = "ILOAdmins"
ldap_search_01 = "OU=IT,OU=ISS,DC=mak,DC=iss"
ldap_search_02 = "CN=Users,DC=mak,DC=iss"
ldap_search_03 = "CN=Builtin,DC=mak,DC=iss"
remote_syslog_server = "10.130.2.11"
snmp_community = "ISS-PUB"
snmp_contact = "Aftab Ahmed"
snmp_location = "Makkah"

# File Variables
dc_resource_list = "Resource List-v7.6.xlsx"
config_template = "OACONFIG.j2"

# Certificate File Variables 
iss_app_cert_file = "iss_app_cert.pem"
iss_nws_cert_file = "iss_nws_cert.pem"

# ==========================================
# 2. Path Setup
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "Templates")
output_dir = os.path.join(base_dir, "oaconfig_scripts")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

excel_file_path = os.path.join(templates_dir, dc_resource_list)

# Load Certificate Contents
app_cert_path = os.path.join(templates_dir, iss_app_cert_file)
nws_cert_path = os.path.join(templates_dir, iss_nws_cert_file)

cert_1_content = ""
if os.path.exists(app_cert_path):
    with open(app_cert_path, 'r', encoding='utf-8') as f:
        cert_1_content = f.read().strip()
else:
    print(f"Warning: Certificate file not found: {app_cert_path}")

cert_2_content = ""
if os.path.exists(nws_cert_path):
    with open(nws_cert_path, 'r', encoding='utf-8') as f:
        cert_2_content = f.read().strip()
else:
    print(f"Warning: Certificate file not found: {nws_cert_path}")

# ==========================================
# 3. Helper Functions
# ==========================================
def generate_rack_name(enc_name):
    try:
        parts = str(enc_name).strip().split('-')
        if len(parts) >= 3 and parts[0] == "SV":
            site = parts[1]
            num_part = parts[2]
            if len(num_part) == 4:
                return f"RA-{site}-A{num_part[1]}-{num_part[2:4]}"
    except Exception as e:
        print(f"Could not parse rack name for {enc_name}: {e}")
    return "UNKNOWN_RACK"

def get_val(row, col_name):
    """Safely retrieves a value, treating 'nan' or 'N.A' as empty."""
    val = str(row.get(col_name, '')).strip()
    if val.lower() == 'nan' or val == 'n.a':
        return ""
    return val

# ==========================================
# 4. Read and Process Excel Data
# ==========================================
print(f"Loading Excel file from: {excel_file_path}")
df = pd.read_excel(excel_file_path, sheet_name="General Resource List", dtype=str, engine="openpyxl")
df.columns = df.columns.str.strip()

# --- VALIDATION: Check for missing columns entirely ---
required_cols = ['equipment_type', 'enclosure_physical_name', 'scope', 'enclosure_slot', 'hostname', 'ilo_ip']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"\n[!] CRITICAL WARNING: The following required columns are missing from the Excel file: {', '.join(missing_cols)}")
    print("The script may fail to extract necessary data.\n")

# Filter down to valid physical names
filtered_df = df[
    (df['enclosure_physical_name'].notna()) & 
    (df['enclosure_physical_name'].str.strip() != 'N.A')
]

enclosures_data = []
current_enclosure = None

for index, row in filtered_df.iterrows():
    # Excel row number for warning messages (+2 accounts for header and 0-index)
    excel_row = index + 2 
    
    eq_type = get_val(row, 'equipment_type')
    enc_phys_name = get_val(row, 'enclosure_physical_name')
    current_scope = get_val(row, 'scope')
    
    # 1. Server Enclosures
    if eq_type == "Server Enclosure":
        # VALIDATION: Check Scope
        if not current_scope:
            print(f"  [!] WARNING (Row {excel_row}): Missing 'scope' for Server Enclosure '{enc_phys_name}'. Network variables will not load.")
            
        enc_name = enc_phys_name
        
        current_enclosure = {
            "enc_name": enc_name,
            "rack_name": generate_rack_name(enc_name),
            "scope": current_scope,
            "oa01_name": "",
            "oa01_ip": "",
            "oa02_name": "",
            "oa02_ip": ""
        }
        
        # Pre-fill all slots to prevent Jinja errors
        for i in range(1, 17):
            current_enclosure[f"name_blade_{str(i).zfill(2)}"] = ""
            current_enclosure[f"ip_blade_{str(i).zfill(2)}"] = ""
        for i in range(1, 9):
            current_enclosure[f"name_interconnect_{str(i).zfill(2)}"] = ""
            current_enclosure[f"interconnect_{str(i).zfill(2)}"] = ""
            
        enclosures_data.append(current_enclosure)
        
    # 2. Components belonging to an enclosure (OAs, Blades, Switches)
    elif eq_type in ["Enclosure OA", "NVR Blade Server", "VCA Blade Server", "Enclosure Switch"] and current_enclosure is not None:
        slot = get_val(row, 'enclosure_slot')
        ip = get_val(row, 'ilo_ip')
        hostname = get_val(row, 'hostname')
        
        # VALIDATION: Check Slots and IPs
        if not slot:
            print(f"  [!] WARNING (Row {excel_row}): Missing 'enclosure_slot' for {eq_type} in enclosure '{current_enclosure['enc_name']}'.")
        if not ip:
            print(f"  [!] WARNING (Row {excel_row}): Missing 'ilo_ip' for {eq_type} (Slot: {slot}) in enclosure '{current_enclosure['enc_name']}'.")
        if not hostname:
            print(f"  [!] WARNING (Row {excel_row}): Missing 'hostname' for {eq_type} (Slot: {slot}) in enclosure '{current_enclosure['enc_name']}'.")

        if slot:
            try:
                # Clean up slot formatting (e.g., '1.0' -> '01')
                slot_clean = str(int(float(slot))).zfill(2)
            except ValueError:
                slot_clean = slot
                
            # Enclosure OAs
            if eq_type == "Enclosure OA":
                if slot_clean == "01":
                    current_enclosure["oa01_name"] = hostname
                    current_enclosure["oa01_ip"] = ip
                elif slot_clean == "02":
                    current_enclosure["oa02_name"] = hostname
                    current_enclosure["oa02_ip"] = ip
            
            # Blades
            elif eq_type in ["NVR Blade Server", "VCA Blade Server"]:
                current_enclosure[f"name_blade_{slot_clean}"] = hostname
                current_enclosure[f"ip_blade_{slot_clean}"] = ip
                
            # Interconnects
            elif eq_type == "Enclosure Switch":
                current_enclosure[f"name_interconnect_{slot_clean}"] = hostname
                current_enclosure[f"interconnect_{slot_clean}"] = ip

# ==========================================
# 5. Render Jinja Templates
# ==========================================
print(f"\nSetting up Jinja environment targeting: {templates_dir}")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template(config_template)

base_vars = {
    "domain": domain, 
    "ilo_admin_group": ilo_admin_group, 
    "ldap_search_01": ldap_search_01,
    "ldap_search_02": ldap_search_02, 
    "ldap_search_03": ldap_search_03,
    "remote_syslog_server": remote_syslog_server, 
    "snmp_community": snmp_community,
    "snmp_contact": snmp_contact, 
    "snmp_location": snmp_location,
    "cert_1": cert_1_content, 
    "cert_2": cert_2_content
}

print(f"Generating configuration files in: {output_dir}")
for enc in enclosures_data:
    if not enc["enc_name"]:
        continue
    
    enc_scope = enc.get("scope", "")
    network_vars = scope_vars.get(enc_scope, {})
    
    if not network_vars:
        print(f"  -> Skipping generation: {enc['enc_name']} (Unknown or missing scope: '{enc_scope}')")
        continue
        
    render_vars = {**base_vars, **network_vars, **enc}
    rendered_config = template.render(render_vars)
    
    output_filename = f"{enc['enc_name']}.txt"
    output_filepath = os.path.join(output_dir, output_filename)
    
    file_exists = os.path.exists(output_filepath)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(rendered_config)
        
    if file_exists:
        print(f"  -> Successfully overwritten: {output_filename} [{enc_scope}]")
    else:
        print(f"  -> Successfully generated: {output_filename} [{enc_scope}]")

print("\nDone.")