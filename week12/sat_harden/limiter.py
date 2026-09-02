import os, datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
DAILY_LIMIT = 3

def record(user, action, outcome, ms=None):
    row = {"user_id": user, "action": action, "outcome": outcome}
    if ms is not None:
        row["ms"] = ms
    sb.table("audit_log").insert(row).execute()

def allow(user, action="fetch"):
    today = str(datetime.date.today())
    r = sb.table("daily_usage").select("count").eq("user_id", user).eq("day", today).execute()
    used = r.data[0]["count"] if r.data else 0
    if used >= DAILY_LIMIT:
        record(user, action, "REFUSED: daily limit")
        return False
    sb.table("daily_usage").upsert({"user_id": user, "day": today, "count": used + 1}).execute()
    record(user, action, "ALLOWED")
    return True