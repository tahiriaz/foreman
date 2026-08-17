import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# ==========================================
# 1. Variables Definition
# ==========================================
gateway = "10.102.18.1"
mask = "255.255.254.0"
dns1 = "10.130.4.11"
dns2 = "10.130.4.12"
ntp1 = "10.102.18.1"
ntp2 = "10.130.2.11"
domain = "mak.iss"
domain_controller = "INFCOSADU001RP.mak.iss"
ilo_admin_group = "ILOAdmins"
ldap_search_01 = "OU=IT,OU=ISS,DC=mak,DC=iss"
ldap_search_02 = "CN=Users,DC=mak,DC=iss"
ldap_search_03 = "CN=Builtin,DC=mak,DC=iss"
remote_syslog_server = "10.130.4.11"
snmp_community = "ISS-PUB"
snmp_contact = "Aftab Ahmed"
snmp_location = "Makkah"

dc_resource_list = "Resource List-v7.4.xlsx"
config_template = "OACONFIG.j2"
scope_var = "RTR"

# Certificate File Variables (Update these if your filenames are different)
iss_app_cert_file = "iss_app_cert.pem"
iss_nws_cert_file = "iss_nws_cert.pem"

# ==========================================
# 2. Path Setup
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "Templates")
output_dir = os.path.join(base_dir, "output")

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

# ==========================================
# 4. Read and Process Excel Data
# ==========================================
print(f"Loading Excel file from: {excel_file_path}")
df = pd.read_excel(excel_file_path, sheet_name="General Resource List", dtype=str, engine="openpyxl")
df.columns = df.columns.str.strip()

filtered_df = df[
    (df['scope'] == scope_var) & 
    (df['enclosure_physical_name'].notna()) & 
    (df['enclosure_physical_name'].str.strip() != 'N.A')
]

enclosures_data = []
current_enclosure = None

for index, row in filtered_df.iterrows():
    eq_type = str(row.get('equipment_type', '')).strip()
    enc_phys_name = str(row.get('enclosure_physical_name', '')).strip()
    
    # 1. Server Enclosures
    if eq_type == "Server Enclosure":
        enc_name = enc_phys_name
        
        current_enclosure = {
            "enc_name": enc_name,
            "rack_name": generate_rack_name(enc_name),
            "oa01_name": "",
            "oa01_ip": "",
            "oa02_name": "",
            "oa02_ip": ""
        }
        
        # Pre-fill all 16 blade slots with empty strings
        for i in range(1, 17):
            slot_str = str(i).zfill(2)
            current_enclosure[f"name_blade_{slot_str}"] = ""
            current_enclosure[f"ip_blade_{slot_str}"] = ""
            
        # Pre-fill all 8 interconnect slots with empty strings
        for i in range(1, 9):
            slot_str = str(i).zfill(2)
            current_enclosure[f"name_interconnect_{slot_str}"] = ""
            current_enclosure[f"interconnect_{slot_str}"] = ""
            
        enclosures_data.append(current_enclosure)
        
    # 2. Enclosure OA
    elif eq_type == "Enclosure OA" and current_enclosure is not None:
        slot = str(row.get('enclosure_slot', '')).strip()
        if slot in ["01", "1", "1.0"]:
            current_enclosure["oa01_name"] = str(row.get('hostname', '')).strip()
            current_enclosure["oa01_ip"] = str(row.get('ilo_ip', '')).strip()
        elif slot in ["02", "2", "2.0"]:
            current_enclosure["oa02_name"] = str(row.get('hostname', '')).strip()
            current_enclosure["oa02_ip"] = str(row.get('ilo_ip', '')).strip()

    # 3. Blades (NVR or VCA)
    elif eq_type in ["NVR Blade Server", "VCA Blade Server"] and current_enclosure is not None:
        slot = str(row.get('enclosure_slot', '')).strip()
        try:
            slot = str(int(float(slot))).zfill(2)
        except ValueError:
            pass
        current_enclosure[f"name_blade_{slot}"] = str(row.get('hostname', '')).strip()
        current_enclosure[f"ip_blade_{slot}"] = str(row.get('ilo_ip', '')).strip()

    # 4. Enclosure Switches (Interconnects)
    elif eq_type == "Enclosure Switch" and current_enclosure is not None:
        slot = str(row.get('enclosure_slot', '')).strip()
        try:
            slot = str(int(float(slot))).zfill(2)
        except ValueError:
            pass
        current_enclosure[f"name_interconnect_{slot}"] = str(row.get('hostname', '')).strip()
        current_enclosure[f"interconnect_{slot}"] = str(row.get('ilo_ip', '')).strip()

# ==========================================
# 5. Render Jinja Templates
# ==========================================
print(f"Setting up Jinja environment targeting: {templates_dir}")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template(config_template)

base_vars = {
    "gateway": gateway, "mask": mask, "dns1": dns1, "dns2": dns2,
    "ntp1": ntp1, "ntp2": ntp2, "domain": domain, "domain_controller": domain_controller,
    "ilo_admin_group": ilo_admin_group, "ldap_search_01": ldap_search_01,
    "ldap_search_02": ldap_search_02, "ldap_search_03": ldap_search_03,
    "remote_syslog_server": remote_syslog_server, "snmp_community": snmp_community,
    "snmp_contact": snmp_contact, "snmp_location": snmp_location,
    "cert_1": cert_1_content, "cert_2": cert_2_content
}

print(f"Generating configuration files in: {output_dir}")
for enc in enclosures_data:
    if not enc["enc_name"]:
        continue
        
    render_vars = {**base_vars, **enc}
    rendered_config = template.render(render_vars)
    
    output_filename = f"{enc['enc_name']}.txt"
    output_filepath = os.path.join(output_dir, output_filename)
    
    file_exists = os.path.exists(output_filepath)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(rendered_config)
        
    if file_exists:
        print(f"  -> Successfully overwritten: {output_filename}")
    else:
        print(f"  -> Successfully generated: {output_filename}")

print("Done.")