import sys
sys.path.append("../thu_scraper")

from scrape import scrape as old_scrape
from scrape2 import scrape as new_scrape

URL = "https://en.wikipedia.org/wiki/Kerala"

try:
    old = old_scrape(URL)
    print("OLD CHARS:", len(old))
    print("OLD FIRST 300:", old[:300])
except Exception as e:
    print("OLD FAILED:", type(e).__name__)

print()
new = new_scrape(URL)
print("NEW CHARS:", len(new))
print("NEW FIRST 300:", new[:300])