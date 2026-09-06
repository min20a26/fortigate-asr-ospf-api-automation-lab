import json
import ssl
import urllib.request
from getpass import getpass

fg = "https://192.168.30.1"
token = getpass("Enter FortiGate API token: ")

# Lab only: the FortiGate uses a self-signed certificate.
# In production, use a trusted certificate and keep TLS verification enabled.
context = ssl._create_unverified_context()

url = f"{fg}/api/v2/monitor/system/status"

request = urllib.request.Request(url)
request.add_header("Authorization", "Bearer " + token)

with urllib.request.urlopen(request, context=context) as response:
    data = json.loads(response.read().decode())

print("Status:", data["status"])
print("Hostname:", data["results"]["hostname"])
print("Model:", data["results"]["model_number"])
print("FortiOS Version:", data["version"])
print("Build:", data["build"])
