import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

rows = sb.table("audit_log").select("*").execute()
print("rows before:", len(rows.data))

target = rows.data[0]["id"]
print("attempting to delete id:", target)
sb.table("audit_log").delete().eq("id", target).execute()

rows = sb.table("audit_log").select("*").execute()
print("rows after:", len(rows.data))