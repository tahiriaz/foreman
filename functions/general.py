import pandas as pd
from functions import process_vm
from functions import process_host
from functions import generic
from functions import vars

valid_resource = [
    'ESXi',
    'NVR',
    'NVR Blade Server',
    'VCA',
    'VCA Blade Server',
    'Virtual Machine',
    'Virtual IP'
]



def provision_from_excel(file_path, sheet, start_row, end_row):
    df = pd.read_excel(file_path, sheet_name=sheet, skiprows=range(1, start_row - 1), nrows=(end_row - start_row + 1),engine='openpyxl')
    # vm_list_na = df.to_dict(orient='records')
    vm_list = (df.fillna('NODATAFOUND')).to_dict(orient='records')
    for vm in vm_list:
        for resource in valid_resource:
            if vm["equipment_type"] == resource:
                if vm["type"] == 'phy':
                    process_host.create(vm)
                if vm["type"] == 'vm':
                    process_vm.create(vm)
                if vm["type"] == 'vip':
                    generic.create_dns_records(vm)

    # for entry in vars.DNS_LIST:
    #     print(entry)
