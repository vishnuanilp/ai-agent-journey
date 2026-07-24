import asyncio, os
from supabase import create_async_client
from dotenv import load_dotenv

load_dotenv()

def handler(payload):
    record = payload.get("data", {}).get("record", payload)
    print("NEW QUESTION:", record.get("question"))

async def main():
    sb = await create_async_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    res = await sb.auth.sign_in_with_password({
        "email": os.getenv("SUPABASE_EMAIL"),
        "password": os.getenv("SUPABASE_PASSWORD"),
    })
    await sb.realtime.set_auth(res.session.access_token)
    channel = sb.channel("conv")
    await channel.on_postgres_changes(
        event="INSERT", schema="public", table="conversations", callback=handler
    ).subscribe()
    await asyncio.sleep(300)

asyncio.run(main())