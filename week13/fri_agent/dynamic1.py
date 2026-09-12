import requests

URL = "https://example.com"
NEEDLE = "without needing permission"

headers = {"User-Agent": "VocviewBot/0.1 (+https://vocview.com)"}
r = requests.get(URL, headers=headers, timeout=10)
r.raise_for_status()

print("STATUS:", r.status_code)
print("LENGTH:", len(r.text))
print("NEEDLE:", NEEDLE)
print("FOUND :", NEEDLE.lower() in r.text.lower())