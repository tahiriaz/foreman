import ssl
import pprint

# Create a default SSL context
context = ssl.create_default_context()

# Retrieve all loaded CA certificates
trusted_certs = context.get_ca_certs()

print(f"Total trusted certificates: {len(trusted_certs)}\n")

# Print the subject (name) of the first 5 certificates as an example
for cert in trusted_certs[:5]:
    pprint.pprint(cert['subject'])