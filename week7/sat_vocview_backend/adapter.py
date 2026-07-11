import anthropic
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import os



load_dotenv()
client = anthropic.Anthropic()
openai_client = OpenAI()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm(prompt, provider):
    if provider == "claude":
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    
    elif provider == "openai":
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    
    elif provider == "gemini":
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    
    raise ValueError(f"Unknown provider: {provider}")

if __name__ == "__main__":
            answer = call_llm("Say hello in one short sentence.", "claude")
            answer = call_llm("Say hello in one short sentence.", "openai")
            answer = call_llm("Say hello in one short sentence.", "gemini")
            print(answer)
       