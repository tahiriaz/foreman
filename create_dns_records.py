## To be used for creating DNS recods only

import os
import pandas as pd
from functions import generic

RESOURCE_LIST = os.path.join(os.path.expanduser('~'), 'Downloads', 'Ressource List-v7.3.xlsx')
SHEET_NAME = "General Resource List"

def dns_from_excel(file_path, sheet, start_row, end_row):
    df = pd.read_excel(file_path, sheet_name=sheet, skiprows=range(1, start_row - 1), nrows=(end_row - start_row + 1),engine='openpyxl')
    vm_list = (df.fillna('NODATAFOUND')).to_dict(orient='records')
    for vm in vm_list:
        generic.create_dns_records(vm)

dns_from_excel(RESOURCE_LIST, SHEET_NAME, 15, 33)