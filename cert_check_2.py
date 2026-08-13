import certifi

# Print the exact path Python is using for the certificate bundle
cert_path = certifi.where()
print(f"Loading certificates from: {cert_path}\n")

# Read and count how many individual certificates are in the file
with open(cert_path, 'r') as file:
    bundle_data = file.read()
    cert_count = bundle_data.count('-----BEGIN CERTIFICATE-----')
    
print(f"Total trusted certificates in bundle: {cert_count}")

# Check if your specific corporate CA was successfully appended
target_ca_name = "Fortinet" # Change this to your CA name to search the file
if target_ca_name in bundle_data:
    print(f"\nSuccess: Found '{target_ca_name}' in the CA bundle.")
else:
    print(f"\nWarning: '{target_ca_name}' is not in the CA bundle.")