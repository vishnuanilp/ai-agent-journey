import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

async def stream_tokens(prompt: str):
    response = await get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in response:
        piece = chunk.choices[0].delta.content
        if piece:
            yield piece