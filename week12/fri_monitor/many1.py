# many1.py — generate a realistic spread of rows
import os, time, random
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
db = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

for i in range(20):
    ms = random.choice([180, 220, 300, 250, 190, 5200])
    outcome = "REFUSED: daily limit" if i % 5 == 0 else "ALLOWED"
    db.table("audit_log").insert({
        "user_id": "ammu_stores", "action": "fetch",
        "outcome": outcome, "ms": ms
    }).execute()

print("inserted 20 rows")