import os

req_bundle = os.environ.get('REQUESTS_CA_BUNDLE')
curl_bundle = os.environ.get('CURL_CA_BUNDLE')

if req_bundle or curl_bundle:
    print(f"WARNING: requests is being overridden!")
    print(f"REQUESTS_CA_BUNDLE: {req_bundle}")
    print(f"CURL_CA_BUNDLE: {curl_bundle}")
else:
    print("No overrides detected. requests will use certifi by default.")