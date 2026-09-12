import requests, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://example.com"
MAX_PAGES = 3
seen = 0

while url and seen < MAX_PAGES:
    r = requests.get(url, timeout=10)
    print("FETCHED :", url, "|", r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    seen += 1
    nxt = soup.find("a", string="Next")
    url = urljoin(url, nxt.get("href")) if nxt else None
    time.sleep(1)

print("PAGES :", seen, "| STOPPED BECAUSE :", "no next link" if not url else "hit cap")