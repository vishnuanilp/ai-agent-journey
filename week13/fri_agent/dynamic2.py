import requests

URL = "https://en.wikipedia.org/wiki/Kerala"
NEEDLE = "Kerala"

headers = {"User-Agent": "VocviewBot/0.1 (+https://vocview.com)"}
r = requests.get(URL, headers=headers, timeout=10)
r.raise_for_status()

pos = r.text.lower().find(NEEDLE.lower() + " is a")
print("STATUS:", r.status_code)
print("LENGTH:", len(r.text))
print("POSITION:", pos)
print("---- 400 CHARS AROUND IT ----")
print(r.text[pos:pos+400] if pos != -1 else "NOT FOUND AT ALL")