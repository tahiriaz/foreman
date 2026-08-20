## To be used for creating DNS recods only

import os
import pandas as pd
from functions import generic

# Get the absolute path of the directory containing the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the Templates folder relative to the script
RESOURCE_LIST = os.path.join(SCRIPT_DIR, 'Templates', 'Resource List-v7.6.xlsx')
SHEET_NAME = "General Resource List"

def dns_from_excel(file_path, sheet, start_row, end_row):
    df = pd.read_excel(file_path, sheet_name=sheet, skiprows=range(1, start_row - 1), nrows=(end_row - start_row + 1),engine='openpyxl')
    vm_list = (df.fillna('NODATAFOUND')).to_dict(orient='records')
    for vm in vm_list:
        generic.create_dns_records(vm)

dns_from_excel(RESOURCE_LIST, SHEET_NAME, 27, 40)