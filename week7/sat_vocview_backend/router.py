import asyncio
from adapter import call_llm

LADDER = ["claude", "openai", "gemini"]

async def route(prompt):
    for provider in LADDER:
        try:
            answer = await call_llm(prompt, provider)
            return answer
        except Exception as e:
            print(f"{provider} failed: {e} — falling back")
    raise RuntimeError("All providers failed")

if __name__ == "__main__":
    print(asyncio.run(route("Say hello in one short sentence.")))