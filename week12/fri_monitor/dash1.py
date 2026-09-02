# dash1.py — turn many rows into a few numbers
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
db = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

rows = db.table("audit_log").select("*").execute().data
timed = [r["ms"] for r in rows if r["ms"] is not None]
refused = [r for r in rows if r["outcome"].startswith("REFUSED")]

print("total requests :", len(rows))
print("refused        :", len(refused))
print("slowest ms     :", max(timed))
print("average ms     :", int(sum(timed) / len(timed)))