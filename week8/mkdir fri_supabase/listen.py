import asyncio, os
from dotenv import load_dotenv
from supabase import create_async_client

load_dotenv()

def handler(payload):
    print("NEW ROW:", payload)



async def main():
    sb = await create_async_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    res = await sb.auth.sign_in_with_password({
        "email": os.getenv("SUPABASE_EMAIL"),
        "password": os.getenv("SUPABASE_PASSWORD")
    })
    await sb.realtime.set_auth(res.session.access_token)
    ch = sb.channel("orders-changes")
    await ch.on_postgres_changes(event="INSERT", schema="public", table="orders", callback=handler).subscribe()
    print("Listening...")
    await asyncio.sleep(300)

   

asyncio.run(main())