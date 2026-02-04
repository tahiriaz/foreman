import requests
from requests.auth import HTTPBasicAuth

def get_hostgroup_id(foreman_url,user,password,hostgroup_name):
    url = f"{foreman_url}/api/v2/hostgroups"
    params = {
        "search": f"name = \"{hostgroup_name}\"",
        "per_page": 1
    }
    try:
        response = requests.get(
            url,
            auth=(user, password),
            params=params,
            verify=True # Set to False if using self-signed certs
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data['results']:
            hostgroup_id = data['results'][0]['id']
            return hostgroup_id
        else:
            print(f"Hostgroup '{hostgroup_name}' not found.")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def get_subnet_id(foreman_url,user,password,subnet_name):
    url = f"{foreman_url}/api/v2/subnets"
    params = {'search': f'name = {subnet_name}'}
    
    try:
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(user, password), 
            params=params, 
            verify=True # Set to True if using valid SSL certificates
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data['results']:
            subnet_id = data['results'][0]['id']
            print(f"Subnet: {subnet_name}, ID: {subnet_id}")
            return subnet_id
        else:
            print(f"Subnet '{subnet_name}' not found.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_organization_id(foreman_url,user,password,org_name):
    # API endpoint to list organizations
    url = f"{foreman_url}/api/organizations"
    
    try:
        # Send GET request
        response = requests.get(
            url,
            auth=HTTPBasicAuth(user, password),
            verify=True # Set to False if using self-signed certificates
        )
        response.raise_for_status() # Raise exception for HTTP errors
        
        orgs = response.json().get('results', [])
        
        # Search for the organization by name
        for org in orgs:
            if org['name'] == org_name:
                return org['id']
                
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def get_location_id(foreman_url,user,password,location_name):
    url = f"{foreman_url}/api/locations"
    
    # Send request with basic authentication
    try:
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(user, password),
            verify=True # Set to False if using self-signed certs
        )
        response.raise_for_status()
        locations = response.json().get('results', [])
        
        # Find the specific location ID by name
        for loc in locations:
            if loc['name'] == location_name:
                return loc['id']
                
        print(f"Location '{location_name}' not found.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_domain_id(foreman_url,user,password,domain_name):
    url = f"{foreman_url}/api/domains"
    
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(user, password),
            verify=True # Set to False if using self-signed certs
        )
        response.raise_for_status()
        data = response.json()
        
        for domain in data['results']:
            if domain['name'] == domain_name:
                return domain['id']   
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None