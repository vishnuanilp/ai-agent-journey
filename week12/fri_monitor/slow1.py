# slow1.py — timing by hand
import time

def fetch_page():
    time.sleep(2)
    return "Ammu Stores price list"

start = time.time()
page = fetch_page()
duration = time.time() - start

print("Got:", page)
print("Took:", round(duration, 2), "seconds")