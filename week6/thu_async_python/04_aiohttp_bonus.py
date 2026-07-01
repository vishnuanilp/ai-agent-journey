import asyncio
import time
import aiohttp

async def fetch_post(session, post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    print(f"  → Fetching post {post_id}")
    async with session.get(url) as response:
        data = await response.json()
    print(f"  ← Got post {post_id}: '{data['title'][:40]}...'")
    return data

async def main():
    print("=== AIOHTTP PARALLEL FETCH ===")
    start = time.time()

    post_ids = [1, 2, 3, 4, 5]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_post(session, pid) for pid in post_ids]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"\nFetched {len(results)} posts in {elapsed:.2f} seconds")
    print(f"First post author user_id: {results[0]['userId']}")

asyncio.run(main())

