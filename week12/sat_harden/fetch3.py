import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Hotel"
HEADERS = {"User-Agent": "VocviewListenToTheWeb/0.1 (vishnu@example.com)"}

resp = requests.get(URL, timeout=10, headers=HEADERS)
if resp.status_code != 200:
    raise SystemExit("REFUSED: " + str(resp.status_code))

soup = BeautifulSoup(resp.text, "html.parser")
body = soup.select_one("#mw-content-text")
text = body.get_text(" ", strip=True)

print("text length:", len(text))
print(text[:500])