import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

row = {
    "owner_id": "6c4986bc-e2a6-4e4a-aaf2-bea7a2e0875c",
    "frame_name": "TEST_DELETE_ME.jpg",
    "outcome": "rejected",
    "reason": "too_dark",
    "crushed": 0.404,
    "person_present": None,
    "person_count": None,
}
print(sb.table("events").insert(row).execute())