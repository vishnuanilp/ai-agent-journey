import time
import requests

UA = "VocviewBot/0.1 (+https://vocview.com)"
MAX_TRIES = 3

def fetch(url):
    wait = 1
    for attempt in range(1, MAX_TRIES + 1):
        r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
        print("ATTEMPT", attempt, "STATUS", r.status_code)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 503):
            if attempt == MAX_TRIES:
                break
            print("  BACKOFF", wait, "s")
            time.sleep(wait)
            wait = wait * 2
            continue
        print("  GIVING UP: status not retryable")
        return None
    print("  GIVING UP: out of attempts")
    return None