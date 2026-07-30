import os
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()

_clients = {}

def get_client(provider):
    if provider not in _clients:
        if provider == "claude":
            _clients[provider] = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "openai":
            _clients[provider] = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "gemini":
            _clients[provider] = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _clients[provider]

async def call_llm(prompt, provider):
    if provider == "claude":
        response = await get_client("claude").messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    elif provider == "openai":
        response = await get_client("openai").chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    elif provider == "gemini":
        response = await get_client("gemini").aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    raise ValueError(f"Unknown provider: {provider}")