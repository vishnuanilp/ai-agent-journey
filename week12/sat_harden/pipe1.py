import requests
from bs4 import BeautifulSoup
from urlcheck import check_url
from sanitize import sanitize

URL = "https://en.wikipedia.org/wiki/Hotel"
HEADERS = {"User-Agent": "VocviewListenToTheWeb/0.1 (vishnu@example.com)"}

ok, why = check_url(URL)
print("urlcheck:", ok, why)
if not ok:
    raise SystemExit("REFUSED at urlcheck")

resp = requests.get(URL, timeout=10, headers=HEADERS)
print("status:", resp.status_code)
if resp.status_code != 200:
    raise SystemExit("REFUSED: " + str(resp.status_code))

raw = BeautifulSoup(resp.text, "html.parser").select_one("#mw-content-text").get_text(" ", strip=True)
clean, log = sanitize(raw)
print("fetched:", len(raw), "-> sanitized:", len(clean))
print("log:", log)