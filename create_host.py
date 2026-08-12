import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from functions import general

# Foreman API configuration

RESOURCE_LIST = 'C:/Users/tahir/Downloads/Ressource List-v7.2.xlsx'
SHEET_NAME = "General Resource List"

general.provision_from_excel(RESOURCE_LIST, SHEET_NAME, 18, 19)

