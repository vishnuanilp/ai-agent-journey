import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
OWNER = "6c4986bc-e2a6-4e4a-aaf2-bea7a2e0875c"

rows = sb.table("events").select("*").eq("owner_id", OWNER)\
        .order("id", desc=True).limit(3).execute().data

for r in rows:
    print(r["id"], r["frame_name"], r["outcome"])
    print("   reason:", r["reason"])