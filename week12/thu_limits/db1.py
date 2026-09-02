import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
print("url:", url)
print("key present:", bool(key))

sb = create_client(url, key)
rows = sb.table("daily_usage").select("*").execute()
print("daily_usage rows:", rows.data)