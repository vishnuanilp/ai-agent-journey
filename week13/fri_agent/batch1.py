import time
from scrape2 import scrape

DELAY = 1
MIN_DOC = 500

def scrape_many(urls):
    good, bad = [], []
    for url in urls:
        try:
            text = scrape(url)
            if len(text) < MIN_DOC:
                bad.append((url, f"too short: {len(text)}"))
            else:
                good.append((url, text))
        except Exception as e:
            bad.append((url, type(e).__name__))
        time.sleep(DELAY)
    print("OK:", len(good), "FAILED:", len(bad), "OF", len(urls))
    return good, bad