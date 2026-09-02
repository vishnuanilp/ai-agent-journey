# dash2.py — count the bad ones instead of averaging
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
db = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

SLOW_MS = 1000
rows = db.table("audit_log").select("*").execute().data
timed = [r["ms"] for r in rows if r["ms"] is not None]
slow = [m for m in timed if m > SLOW_MS]

print("timed requests :", len(timed))
print("slower than", SLOW_MS, "ms:", len(slow))
print("percent slow   :", round(100 * len(slow) / len(timed)), "%")