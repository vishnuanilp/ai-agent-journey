import asyncio
from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    message = await websocket.receive_text()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
    )
    reply = response.choices[0].message.content
    for word in reply.split():
        await websocket.send_text(word)
        await asyncio.sleep(0.1)