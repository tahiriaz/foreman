import requests
import os
import pandas as pd
from requests.auth import HTTPBasicAuth
from functions import general

# Foreman API configuration

# Get the absolute path of the directory containing the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the Templates folder relative to the script
RESOURCE_LIST = os.path.join(SCRIPT_DIR, 'Templates', 'Resource List-v7.4.xlsx')
SHEET_NAME = "General Resource List"

general.provision_from_excel(RESOURCE_LIST, SHEET_NAME, 174, 181)

