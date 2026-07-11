import os
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = AsyncAnthropic()
openai_client = AsyncOpenAI()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def call_llm(prompt, provider):
    if provider == "claude":
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    elif provider == "openai":
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    elif provider == "gemini":
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text

    raise ValueError(f"Unknown provider: {provider}")