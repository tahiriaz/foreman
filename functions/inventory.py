import pandas as pd

from functions import vars
from functions.shared import is_valid


# ---------------------------------------------------------
# INVENTORY SCHEMA
# ---------------------------------------------------------

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

# Keep the valid resource list automatically aligned with REQUIRED_COLUMNS.
VALID_RESOURCES = set(REQUIRED_COLUMNS)


def load_inventory(file_path=None, sheet=None, start_row=None, end_row=None):
    file_path = vars.RESOURCE_LIST if file_path is None else file_path
    sheet = vars.SHEET_NAME if sheet is None else sheet
    start_row = vars.START_ROW if start_row is None else start_row
    end_row = vars.END_ROW if end_row is None else end_row

    print("Loading inventory from Excel rows {} through {}...".format(
        start_row,
        end_row,
    ))

    df = pd.read_excel(
        file_path,
        sheet_name=sheet,
        skiprows=range(1, start_row - 1),
        nrows=end_row - start_row + 1,
        engine=vars.EXCEL_ENGINE,
    )

    return df.fillna(vars.EMPTY_VALUE).to_dict(orient="records")


def validate_resource(vm, excel_row):
    eq_type = str(vm.get("equipment_type", "")).strip()
    logical_name = str(
        vm.get("logical_name", vm.get("hostname", "Unknown"))
    ).strip()

    if eq_type not in VALID_RESOURCES:
        return {
            "valid": False,
            "status": "Skipped",
            "details": "Invalid or missing equipment_type '{}'.".format(
                eq_type
            ),
            "equipment_type": eq_type,
            "logical_name": logical_name,
        }

    missing = [
        col for col in REQUIRED_COLUMNS.get(eq_type, [])
        if not is_valid(vm.get(col))
    ]

    if missing:
        return {
            "valid": False,
            "status": "Skipped",
            "details": "Missing required data in columns: " + ", ".join(missing),
            "equipment_type": eq_type,
            "logical_name": logical_name,
        }

    vm["_excel_row"] = excel_row

    return {
        "valid": True,
        "equipment_type": eq_type,
        "logical_name": logical_name,
    }
