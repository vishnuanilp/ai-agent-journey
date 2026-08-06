import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
OWNER = "6c4986bc-e2a6-4e4a-aaf2-bea7a2e0875c"

def get_events():
    db = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    r = db.table("events").select("*").eq("owner_id", OWNER).execute()
    return r.data

if __name__ == "__main__":
    for row in get_events():
        print(row)