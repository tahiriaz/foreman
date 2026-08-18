import requests

response = requests.get(
    "https://idsfrk02.mak.iss",
    verify=r"D:\Certs\combined.pem"
)

print(response.status_code)