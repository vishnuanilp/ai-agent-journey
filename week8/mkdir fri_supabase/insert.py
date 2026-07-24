from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

response = supabase.table("orders").insert({"item": "Chicken Biryani", "quantity": 2}).execute()
print(response)