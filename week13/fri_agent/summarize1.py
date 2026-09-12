import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
LIMIT = 5000
_client = None

def summarize(text, lang="English"):
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    clipped = text[:LIMIT]
    print("KEPT", len(clipped), "OF", len(text), "CHARS")
    r = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Summarise the article in exactly 3 short sentences. Reply only in {lang}."},
            {"role": "user", "content": clipped}])
    return r.choices[0].message.content