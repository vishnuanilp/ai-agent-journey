import asyncio
import websockets

async def main():
    async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
        await websocket.send("Table for four at 8pm?")
        try:
            while True:
                word = await websocket.recv()
                print(word)
        except websockets.exceptions.ConnectionClosed:
            print("--- stream finished ---")

asyncio.run(main())