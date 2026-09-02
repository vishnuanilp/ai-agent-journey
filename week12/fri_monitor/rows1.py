# rows1.py — what does audit_log actually look like?
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
db = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

result = db.table("audit_log").select("*").execute()

for row in result.data:
    print(row)