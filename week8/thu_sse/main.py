from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def event_stream():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Confirm a table for four at 8pm"}],
    )
    reply = response.choices[0].message.content
    for word in reply.split():
        yield f"data: {word}\n\n"
        await asyncio.sleep(0.1)

@app.get("/stream")
async def stream():
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )