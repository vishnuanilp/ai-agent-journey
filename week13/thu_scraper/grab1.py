import requests

url = "https://example.com"
r = requests.get(url, timeout=10)

print("STATUS  :", r.status_code)
print("TYPE    :", type(r.text))
print("LENGTH  :", len(r.text))
print("---- RAW HTML ----")
print(r.text)