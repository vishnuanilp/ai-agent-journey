import asyncio
import time

async def fake_api_call(name, delay):
    print(f"  → {name} started")
    await asyncio.sleep(delay)
    print(f"  ← {name} finished after {delay}s")
    return f"{name} result"

async def run_sequential():
    print("\n=== SEQUENTIAL ===")
    start = time.time()

    await fake_api_call("Call-1", 2)
    await fake_api_call("Call-2", 2)
    await fake_api_call("Call-3", 2)

    elapsed = time.time() - start
    print(f"Sequential total: {elapsed:.2f} seconds")

async def run_parallel():
    print("\n=== PARALLEL ===")
    start = time.time()

    results = await asyncio.gather(
        fake_api_call("Call-1", 2),
        fake_api_call("Call-2", 2),
        fake_api_call("Call-3", 2),
    )

    elapsed = time.time() - start
    print(f"Parallel total: {elapsed:.2f} seconds")
    print(f"Results: {results}")

asyncio.run(run_sequential())
asyncio.run(run_parallel())