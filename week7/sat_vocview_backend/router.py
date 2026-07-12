import asyncio
import logging
from adapter import call_llm

logger = logging.getLogger(__name__)

LADDER = ["claude", "openai", "gemini"]

async def route(prompt):
    for provider in LADDER:
        try:
            logger.info(f"Routing to {provider}")
            answer = await call_llm(prompt, provider)
            return answer
        except Exception as e:
            logger.error(f"{provider} failed: {e} — falling back")
    raise RuntimeError("All providers failed")

if __name__ == "__main__":
    print(asyncio.run(route("Say hello in one short sentence.")))