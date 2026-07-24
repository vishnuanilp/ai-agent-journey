from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
res = supabase.auth.sign_in_with_password({
    "email": os.getenv("SUPABASE_EMAIL"),
    "password": os.getenv("SUPABASE_PASSWORD")
})
data = open("pricelist.txt", "rb").read()
res = supabase.storage.from_("voc").upload("pricelist.txt", data)
print(res)