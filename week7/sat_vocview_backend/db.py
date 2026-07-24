import os
from supabase import create_async_client
from dotenv import load_dotenv

load_dotenv()

_client = None
_owner_id = None

async def get_client():
    global _client
    if _client is None:
        _client = await create_async_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )
    return _client

async def get_owner_id():
    global _owner_id
    if _owner_id is None:
        sb = await get_client()
        res = await sb.auth.sign_in_with_password({
            "email": os.getenv("SUPABASE_EMAIL"),
            "password": os.getenv("SUPABASE_PASSWORD"),
        })
        _owner_id = res.user.id
    return _owner_id

async def save_question(owner_id, question, business_type):
    sb = await get_client()
    res = await sb.table("conversations").insert({
        "owner_id": owner_id,
        "question": question,
        "business_type": business_type,
    }).execute()
    return res.data[0]["id"]

async def save_answer(row_id, answer):
    sb = await get_client()
    await sb.table("conversations").update(
        {"answer": answer}
    ).eq("id", row_id).execute()