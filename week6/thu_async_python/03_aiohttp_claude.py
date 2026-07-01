import asyncio
import time
import os
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

load_dotenv()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def ask_claude(question):
    print(f"  → Asking: {question}")
    response = await client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": question}]
    )
    answer = response.content[0].text
    print(f"  ← Got answer for: {question}")
    return answer

async def run_sequential():
    print("\n=== SEQUENTIAL (one Claude call at a time) ===")
    start = time.time()

    questions = [
        "What is Python in one sentence?",
        "What is a neural network in one sentence?",
        "What is async programming in one sentence?",
        "What is a database in one sentence?",
        "What is an API in one sentence?",
    ]

    for question in questions:
        await ask_claude(question)

    elapsed = time.time() - start
    print(f"Sequential total: {elapsed:.2f} seconds")

async def run_parallel():
    print("\n=== PARALLEL (all Claude calls at once) ===")
    start = time.time()

    questions = [
        "What is Python in one sentence?",
        "What is a neural network in one sentence?",
        "What is async programming in one sentence?",
        "What is a database in one sentence?",
        "What is an API in one sentence?",
    ]

    tasks = [ask_claude(q) for q in questions]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"Parallel total: {elapsed:.2f} seconds")
    print(f"\nFirst answer preview: {results[0][:80]}...")

asyncio.run(run_sequential())
asyncio.run(run_parallel())