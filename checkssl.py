import requests

response = requests.get(
    "https://idsfrk02.mak.iss",
    verify=r"D:\Certs\ISS-Root.cer"
)

print(response.status_code)