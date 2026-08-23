import os
import sys
import json
import subprocess
import requests
import pandas as pd
import dns.resolver
from requests.auth import HTTPBasicAuth

# Local imports
from functions import vars

# ---------------------------------------------------------
# CONSTANTS & CONFIGURATION
# ---------------------------------------------------------

# Set of values considered "empty" or invalid
INVALID_VALUES = {'NODATAFOUND', 'N.A', 'n.a', '', None}

# Converted list to a set for O(1) lookups instead of O(n) iteration
VALID_RESOURCES = {
    'ESXi',
    'NVR',
    'NVR Blade Server',
    'VCA',
    'VCA Blade Server',
    'Virtual Machine',
    'Virtual IP',
    'Enclosure OA',
    'Enclosure Switch',
    'Server Enclosure'
}

# Define column groups for modularity
BASE_COLS = ['scope', 'subsystems', 'function', 'hostname', 'logical_name', 'domain_name']
ALIAS_COLS = ['alias', 'alias_domain']
BOND0_COLS = ['nic0_name', 'nic0_pxe_subnet_name', 'nic0_mac', 'nic1_name', 'nic1_mac', 'bond0_name', 'bond0_type', 'bond0_devs']
BOND1_COLS = ['nic2_name', 'nic2_mac', 'nic3_name', 'nic3_mac', 'bond1_name', 'bond1_type', 'bond1_devs']
BOND2_COLS = ['nic4_name', 'nic4_mac', 'nic5_name', 'nic5_mac', 'bond2_name', 'bond2_type', 'bond2_devs']
FE_COLS = ['fe_logical_naming', 'fe_vlan_id', 'fe_vlan_name', 'fe_netmask', 'fe_ip_address', 'fe_ip_gateway', 'fe_interface_type', 'fe_interface_name', 'fe_attach_to']
ME_COLS = ['me_logical_naming', 'me_vlan_id', 'me_vlan_name', 'me_netmask', 'me_ip_address', 'me_gateway', 'me_interface_type', 'me_interface_name', 'me_attach_to']
BE_COLS = ['be_logical_name', 'be_vlan_id', 'be_vlan_name', 'be_netmask', 'be_ip_address', 'be_ip_gateway', 'be_interface_type', 'be_interface_name', 'be_attach_to']
CL_COLS = ['cl_logical_name', 'cl_vlan_id', 'cl_vlan_name', 'cl_netmask', 'cl_ip_address', 'cl_ip_gateway', 'cl_interface_type', 'cl_interface_name', 'cl_attach_to']
VM_REQ_COLS = ['vm_folder', 'cpu', 'ram_(gb)', 'storage1_disk_size_system', 'storage1_datastore_system', 'virtual_disk_type']
NTP_COLS = ['ntp1', 'ntp2']
FOREMAN_COLS = ['foreman_parameters']
ENCLOSURE_COLS =  ['enclosure_physical_name', 'enclosure_slot']

# Concatenate lists dynamically for cleaner code
REQUIRED_COLUMNS = {
    'ESXi': BASE_COLS + ALIAS_COLS + ['fe_logical_naming', 'fe_ip_address'],
    'Virtual Machine': BASE_COLS + VM_REQ_COLS + ALIAS_COLS + ['fe_vlan_name', 'fe_logical_naming', 'fe_ip_address', 'os_template_name', 'os_template_version'],
    'Virtual IP': BASE_COLS + ALIAS_COLS + ['fe_logical_naming', 'fe_ip_address'],
    'NVR': BASE_COLS + ALIAS_COLS + BOND0_COLS + BOND1_COLS + FE_COLS + ME_COLS + BE_COLS + CL_COLS + FOREMAN_COLS + NTP_COLS + ['variation'],
    'NVR Blade Server': BASE_COLS + ALIAS_COLS + BOND0_COLS + BOND1_COLS + BOND2_COLS + FE_COLS + ME_COLS + BE_COLS + CL_COLS + FOREMAN_COLS + NTP_COLS + ENCLOSURE_COLS + ['variation'],
    'VCA': BASE_COLS + ALIAS_COLS + BOND0_COLS + BOND1_COLS + FE_COLS + ME_COLS + NTP_COLS + ['variation'],
    'VCA Blade Server': BASE_COLS + ALIAS_COLS + BOND0_COLS + FE_COLS + ME_COLS + NTP_COLS + ENCLOSURE_COLS + ['variation'],
    'Server Enclosure': BASE_COLS + ALIAS_COLS + ['enclosure_physical_name'],
    'Enclosure OA': BASE_COLS + ENCLOSURE_COLS,
    'Enclosure Switch': BASE_COLS + ENCLOSURE_COLS,
}

# ---------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------

def get_resource_id(foreman_url, endpoint, user, password, name, key="name"):
    try:
        response = requests.get(
            f"{foreman_url}/{endpoint}",
            auth=(user, password),
            params={"search": f'{key} = "{name}"'}, 
            verify=True,
            timeout=10  # Fails quickly if server is dead, instead of hanging
        )
        response.raise_for_status() # Catches 401 Unauthorized, 404, etc.
        
        results = response.json().get('results', [])
        if not results:
            raise Exception(f"Could not find {endpoint} with {key}: {name}")
        return results[0]['id']
        
    except requests.exceptions.ConnectionError:
        print(f"\n[CRITICAL ERROR] Connection with Foreman host failed at: {foreman_url}")
        print("Please verify your network connection, VPN, and ensure the Foreman server is online.")
        sys.exit(1) # Gracefully exits the script immediately
        
    except requests.exceptions.Timeout:
        print(f"\n[CRITICAL ERROR] Connection to Foreman host timed out after 10 seconds: {foreman_url}")
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        print(f"\n[CRITICAL ERROR] An HTTP error occurred while contacting Foreman: {e}")
        sys.exit(1)

def dump_2_file(data, directory, file_name):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    file_path = os.path.join(directory, file_name)
    try:
        with open(file_path, 'w') as f:
            for item in data:
                f.write(str(item) + '\n')
        return 0
    except IOError as e:
        print(f"Error writing to file: {e}")

def run_dns_script(file_path, dns_server, domain, user, password):
    # Construct the command
    # ExecutionPolicy Bypass ensures the script runs even if restricted
    command = [
        "powershell.exe", 
        "-ExecutionPolicy", "Bypass", 
        "-File", os.path.join(os.path.dirname(os.path.abspath(__file__)), vars.DNS_SCRIPT),
        "-FileName", file_path,
        "-DnsServer", dns_server,
        "-DomainName", domain,
        "-Username", user,
        "-Password", password
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=False)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(result.stderr)
            return False
    except Exception as e:
        print(f"An error occurred while trying to call PowerShell: {e}")
        return False

# ---------------------------------------------------------
# DNS FUNCTIONS
# ---------------------------------------------------------

def dns_chk_hostname(hostname, dnsserver):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dnsserver]

def check_a_record(domain, dnsserver):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dnsserver]
        answers = dns.resolver.resolve(domain, 'A')
        print(f"A record found for {domain}:")
        for rdata in answers:
            print(f"- {rdata.address}")
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        print(f"No A record found for {domain}.")
        return False

def check_cname_record(domain):
    """Checks if a CNAME record exists for the domain."""
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        print(f"CNAME record found for {domain}:")
        for rdata in answers:
            print(f"- Points to: {rdata.target}")
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        print(f"No CNAME record found for {domain}.")
        return False

def check_a_or_cname(domain):
    """Checks if either an A or CNAME record exists."""
    print(f"Checking DNS records for: {domain}")
    has_a = check_a_record(domain)
    has_cname = check_cname_record(domain)

    if has_a or has_cname:
        print(f"Result: {domain} has an A or CNAME record.")
        return True
    else:
        print(f"Result: {domain} does not have an A or CNAME record.")
        return False

def create_dns_records(vm):
    dns_array = ["hostname,RecordType,Target"]
    
    # Leveraged INVALID_VALUES set to clean up conditions
    if vm.get("ilo_hostname") not in INVALID_VALUES and vm.get("ilo_ip") not in INVALID_VALUES:
        dns_array.append(vm["ilo_hostname"] + ",A," + vm["ilo_ip"])
        
    if vm.get("fe_ip_address") not in INVALID_VALUES and vm.get("me_ip_address") not in INVALID_VALUES:
        # Primary interface is ME
        dns_array.append(vm["logical_name"] + ",A," + vm["me_ip_address"])
        dns_array.append(vm["alias_domain"] + ",CNAME," + vm["logical_name"])
        dns_array.append(vm["me_logical_naming"] + ",CNAME," + vm["logical_name"])
        dns_array.append(vm["fe_logical_naming"] + ",A," + vm["fe_ip_address"])
        
        if vm.get("be_ip_address") not in INVALID_VALUES:
            dns_array.append(vm["be_logical_name"] + ",A," + vm["be_ip_address"])
        if vm.get("cl_ip_address") not in INVALID_VALUES:
            dns_array.append(vm["cl_logical_name"] + ",A," + vm["cl_ip_address"])
            
    elif vm.get("fe_ip_address") not in INVALID_VALUES and vm.get("me_ip_address") in INVALID_VALUES:
        # Primary interface is FE
        dns_array.append(vm["logical_name"] + ",A," + vm["fe_ip_address"])
        dns_array.append(vm["alias_domain"] + ",CNAME," + vm["logical_name"])
        dns_array.append(vm["fe_logical_naming"] + ",CNAME," + vm["logical_name"])
        
        if vm.get("be_ip_address") not in INVALID_VALUES:
            dns_array.append(vm["be_logical_name"] + ",A," + vm["be_ip_address"])
        if vm.get("cl_ip_address") not in INVALID_VALUES:
            dns_array.append(vm["cl_logical_name"] + ",A," + vm["cl_ip_address"])
            
    if dump_2_file(dns_array, os.path.dirname(os.path.abspath(__file__)), vars.DNS_FILENAME) == 0:
        print("Successfully generated DNS file for " + vm["logical_name"])
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), vars.DNS_FILENAME)
        
        if run_dns_script(script_path, vars.DNS_SERVER, vars.DOMAIN_NAME, vars.DNS_SERVER_USER, vars.DNS_SERVER_PASS):
            print("Successfully added DNS records for " + vm["logical_name"])

# ---------------------------------------------------------
# FOREMAN / HOST PARAMETER FUNCTIONS
# ---------------------------------------------------------

def gethost_parameters(parameter, ntp1, ntp2):
    rt_param_array = []
    
    # Leveraged INVALID_VALUES set
    if parameter not in INVALID_VALUES:
        param_array = parameter.split(',')
        for params in param_array:
            param_extract = params.split("=", 2)
            if len(param_extract) == 2:
                rt_param_array.append({
                    "name": param_extract[0],
                    "value": param_extract[1]
                })
                
    if ntp1 not in INVALID_VALUES:
        rt_param_array.append({"name": "ntp-server", "value": ntp1})
        
    if ntp2 not in INVALID_VALUES:
        rt_param_array.append({"name": "ntp2", "value": ntp2})
        
    return rt_param_array

def gethostgroup(subs, func, vart):
    mapping = str(subs) + str(func) + str(vart)
    for type_key, hg in vars.hg_map.items():
        if mapping == type_key:
            return hg
    return None

# ---------------------------------------------------------
# MAIN EXECUTION ROUTINES
# ---------------------------------------------------------

def provision_from_excel(file_path, sheet, start_row, end_row):
    # Fix Import Loop: Import these here so they only load AFTER general.py finishes initializing
    from functions import process_vm
    from functions import process_host
    
    # NEW: Dictionary dispatch mapping 'equipment_type' directly to the execution function
    PROCESSOR_MAP = {
        'ESXi': create_dns_records,
        'NVR': process_host.create,
        'NVR Blade Server': process_host.create,
        'VCA': process_host.create,
        'VCA Blade Server': process_host.create,
        'Virtual Machine': process_vm.create,
        'Virtual IP': create_dns_records,
        'Enclosure OA': create_dns_records,
        'Enclosure Switch': create_dns_records,
        'Server Enclosure': create_dns_records
    }

    df = pd.read_excel(
        file_path, 
        sheet_name=sheet, 
        skiprows=range(1, start_row - 1), 
        nrows=(end_row - start_row + 1),
        engine='openpyxl'
    )
    
    vm_list = df.fillna('NODATAFOUND').to_dict(orient='records')
    
    for idx, vm in enumerate(vm_list, start=start_row):
        eq_type = vm.get("equipment_type")
        
        # 1. VALIDATION: Check if it's a valid resource
        if eq_type not in VALID_RESOURCES:
            print(f"WARNING (Row {idx}): Invalid or missing equipment_type '{eq_type}'. Skipping.")
            continue
            
        # 2. VALIDATION: Check required columns for this specific resource type
        req_cols = REQUIRED_COLUMNS.get(eq_type, [])
        missing_or_invalid = []
        
        for col in req_cols:
            val = vm.get(col)
            # Check against explicitly invalid values or completely empty strings
            if val in INVALID_VALUES or str(val).strip() == '' or str(val).strip().upper() == 'N.A':
                missing_or_invalid.append(col)
                
        if missing_or_invalid:
            print(f"WARNING (Row {idx}): Missing required data in columns {missing_or_invalid} for '{eq_type}'. Skipping.")
            continue

        # 3. EXECUTION: Process valid rows using the dictionary map based on equipment_type
        process_func = PROCESSOR_MAP.get(eq_type)
        
        if process_func:
            process_func(vm)
        else:
            print(f"WARNING (Row {idx}): No processing function mapped for equipment_type '{eq_type}'. Skipping.")