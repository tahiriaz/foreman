import requests
import os
import pandas as pd
from requests.auth import HTTPBasicAuth
from functions import general

# Foreman API configuration

# RESOURCE_LIST = 'C:/Users/tahir/Downloads/Ressource List-v7.3.xlsx'
RESOURCE_LIST = os.path.join(os.path.expanduser('~'), 'Downloads', 'Ressource List-v7.3.xlsx')
SHEET_NAME = "General Resource List"

general.provision_from_excel(RESOURCE_LIST, SHEET_NAME, 174, 181)

