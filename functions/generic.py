import requests
from requests.auth import HTTPBasicAuth
from functions import vars
import os
import json
import subprocess
import dns.resolver

def get_resource_id(foreman_url,endpoint,user,password,name,key="name"):
    response = requests.get(
        f"{foreman_url}/{endpoint}",
        auth=(user, password),
        params={f"search": f'{key} = "{name}"'}, 
        verify=True
    )
    results = response.json().get('results', [])
    if not results:
        raise Exception(f"Could not find {endpoint} with {key}: {name}")
    return results[0]['id']

def run_dns_script(file_path, dns_server, domain, user, password):
    # Construct the command
    # ExecutionPolicy Bypass ensures the script runs even if restricted
    command = [
        "powershell.exe", 
        "-ExecutionPolicy", "Bypass", 
        "-File", os.path.join(os.path.dirname(os.path.abspath(__file__)),vars.DNS_SCRIPT),
        "-FileName", file_path,
        "-DnsServer", dns_server,
        "-DomainName", domain,
        "-Username", user,
        "-Password", password
    ]

    try:
        # Run the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=False)

        # Check the Return Code
        if result.returncode == 0:
            # print("PowerShell Status: SUCCESS")
            print(result.stdout)
            return True
        else:
            # print(f"PowerShell Status: FAILED (Code: {result.returncode})")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"An error occurred while trying to call PowerShell: {e}")
        return False

# Example Call

def dns_chk_hostname(hostname,dnsserver):
      resolver = dns.resolver.Resolver()
      resolver.nameservers = [dnsserver]

def check_a_record(domain,dnsserver):
    try:
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
        if vm["ilo_hostname"] != "N.A" and vm["ilo_hostname"] != "NODATAFOUND" and vm["ilo_ip"] != "N.A" and vm["ilo_ip"] != "NODATAFOUND":
            # iLO IP Address
            dns_array.append(vm["ilo_hostname"] + ",A," + vm["ilo_ip"])
        if vm["fe_ip_address"] != "N.A" and vm["fe_ip_address"] != "NODATAFOUND" and vm["me_ip_address"] != "N.A" and vm["me_ip_address"] != "NODATAFOUND":
                # Primary interface is ME
                dns_array.append(vm["logical_name"] + ",A," + vm["me_ip_address"])
                dns_array.append(vm["alias_domain"] + ",CNAME," + vm["logical_name"])
                dns_array.append(vm["me_logical_naming"] + ",CNAME," + vm["logical_name"])
                dns_array.append(vm["fe_logical_naming"] + ",A," + vm["fe_ip_address"])
                if vm["be_ip_address"] != "N.A" and vm["be_ip_address"] != "NODATAFOUND":
                        dns_array.append(vm["be_logical_name"] + ",A," + vm["be_ip_address"])
                if vm["cl_ip_address"] != "N.A" and vm["cl_ip_address"] != "NODATAFOUND":
                        dns_array.append(vm["cl_logical_name"] + ",A," + vm["cl_ip_address"])
        if vm["fe_ip_address"] != "N.A" and vm["fe_ip_address"] != "NODATAFOUND" and (vm["me_ip_address"] == "N.A" or vm["me_ip_address"] == "NODATAFOUND"):
                # Primary interface is FE
                dns_array.append(vm["logical_name"] + ",A," + vm["fe_ip_address"])
                dns_array.append(vm["alias_domain"] + ",CNAME," + vm["logical_name"])
                dns_array.append(vm["fe_logical_naming"] + ",CNAME," + vm["logical_name"])
                if vm["be_ip_address"] != "N.A" and vm["be_ip_address"] != "NODATAFOUND":
                        dns_array.append(vm["be_logical_name"] + ",A," + vm["be_ip_address"])
                if vm["cl_ip_address"] != "N.A" and vm["cl_ip_address"] != "NODATAFOUND":
                        dns_array.append(vm["cl_logical_name"] + ",A," + vm["cl_ip_address"])
        if (dump_2_file(dns_array,os.path.dirname(os.path.abspath(__file__)),vars.DNS_FILENAME)) == 0:
            print("Successfully generated DNS file for " + vm["logical_name"])
            if (run_dns_script(os.path.join(os.path.dirname(os.path.abspath(__file__)),vars.DNS_FILENAME), vars.DNS_SERVER, vars.DOMAIN_NAME, vars.DNS_SERVER_USER, vars.DNS_SERVER_PASS)) == True:
                 print("Successfully added DNS records for " + vm["logical_name"])

def dump_2_file(data,directory,file_name):
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

def gethost_parameters(parameter,ntp1,ntp2):
        rt_param_array = []
        if parameter != "N.A" and parameter != "NODATAFOUND":
            param_array = parameter.split(',')
            for params in param_array:
                    param_extract=params.split("=",2)
                    param_name = param_extract[0]
                    param_value = param_extract[1]
                    param_list = {
                            "name" : param_name,
                            "value" : param_value
                    }
                    rt_param_array.append(param_list)
        if ntp1 != "N.A" and ntp1 != "NODATAFOUND":
            ntp1_list = {
                "name" : "ntp-server",
                "value" : ntp1
            }
            rt_param_array.append(ntp1_list)
        if ntp2 != "N.A" and ntp2 != "NODATAFOUND":
            ntp2_list = {
                "name" : "ntp2",
                "value" : ntp2
            }
            rt_param_array.append(ntp2_list)
        return rt_param_array

def gethostgroup(subs,func,vart):
        map = str(subs) + str(func) + str(vart)
        for type, hg in vars.hg_map.items():
                if map == type:
                        return hg
                