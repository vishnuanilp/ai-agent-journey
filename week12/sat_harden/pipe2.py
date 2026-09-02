import time, requests
from bs4 import BeautifulSoup
from urlcheck import check_url
from sanitize import sanitize
from limiter import allow, record

USER = "hotel_desk"
URL = "https://en.wikipedia.org/wiki/Hotel"
HEADERS = {"User-Agent": "VocviewListenToTheWeb/0.1 (vishnu@example.com)"}

if not allow(USER, "ratelimit"):
    raise SystemExit("REFUSED: daily limit")

ok, why = check_url(URL)
record(USER, "urlcheck", "OK" if ok else "REFUSED: " + why)
if not ok:
    raise SystemExit("REFUSED at urlcheck")

t = time.time()
resp = requests.get(URL, timeout=10, headers=HEADERS)
ms = int((time.time() - t) * 1000)
record(USER, "fetch", "OK " + str(resp.status_code), ms)
print("fetch:", resp.status_code, ms, "ms")

raw = BeautifulSoup(resp.text, "html.parser").select_one("#mw-content-text").get_text(" ", strip=True)
clean, log = sanitize(raw)
record(USER, "sanitize", "truncated " + str(log["truncated"]))
print("sanitize:", len(raw), "->", len(clean), log)