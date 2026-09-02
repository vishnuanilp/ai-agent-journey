import os, datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
DAILY_LIMIT = 3

def allow(user):
    today = str(datetime.date.today())
    r = sb.table("daily_usage").select("count").eq("user_id", user).eq("day", today).execute()
    used = r.data[0]["count"] if r.data else 0
    if used >= DAILY_LIMIT:
        return False
    sb.table("daily_usage").upsert({"user_id": user, "day": today, "count": used + 1}).execute()
    return True

for u in ["asha", "asha", "asha", "asha", "ravi"]:
    print(u, "->", "ALLOWED" if allow(u) else "REFUSED")