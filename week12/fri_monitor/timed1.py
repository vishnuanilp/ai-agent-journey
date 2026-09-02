# timed1.py — measure it, then store the measurement
import os, time
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
db = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def fetch_page():
    time.sleep(2)
    return "Ammu Stores price list"

start = time.time()
page = fetch_page()
ms = int((time.time() - start) * 1000)

db.table("audit_log").insert({
    "user_id": "ravi", "action": "fetch", "outcome": "ALLOWED", "ms": ms
}).execute()
print("stored ms =", ms)