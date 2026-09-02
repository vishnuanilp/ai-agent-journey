import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Hotel"
HEADERS = {"User-Agent": "VocviewListenToTheWeb/0.1 (vishnu@example.com)"}

resp = requests.get(URL, timeout=10, headers=HEADERS)
print("status:", resp.status_code)

if resp.status_code != 200:
    print("REFUSED: server said", resp.status_code)
    raise SystemExit(1)

text = BeautifulSoup(resp.text, "html.parser").get_text()
print("text length:", len(text))
print(text[:500])