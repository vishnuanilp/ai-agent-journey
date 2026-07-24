import asyncio
import time
from adapter import call_llm

async def ask_all(prompt):
    providers = ["claude", "openai", "gemini"]
    tasks = [call_llm(prompt, p) for p in providers]
    return await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = time.time()
    answers = asyncio.run(ask_all("Say hello in one short sentence."))
    print(answers)
    print(f"Parallel took {time.time() - start:.1f}s")