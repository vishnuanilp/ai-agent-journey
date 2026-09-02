# slow2.py — Sentry holds the stopwatch
import os
import time
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)

def fetch_page():
    time.sleep(2)
    return "Ammu Stores price list"

with sentry_sdk.start_transaction(name="fetch_shop_page"):
    page = fetch_page()

print("Got:", page)