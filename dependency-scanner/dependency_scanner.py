import requests

url = "https://api.osv.dev/v1/query"
payload = {"package": {"name": "werkzeug", "ecosystem": "PyPI"}}

response = requests.post(url, json=payload)
data = response.json()

# Liste aller Schwachstellen extrahieren
vulnerabilities = data.get("vulns", [])

print(vulnerabilities[0])

for vulnerability in vulnerabilities:

    for alias in vulnerability["aliases"]:
        if alias.startswith("CVE-"):
            id = vulnerability["aliases"][alias]

    if (id != None):
        id = vulnerability.get("id")

    print(id)