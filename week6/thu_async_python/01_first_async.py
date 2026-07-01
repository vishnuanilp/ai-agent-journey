import asyncio

async def say_hello():
    print("Starting...")
    await asyncio.sleep(2)
    print("Finished after 2 seconds!")

asyncio.run(say_hello())