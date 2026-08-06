import base64, os, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT = """Look at this image. Reply ONLY with JSON:
{"person_present": true/false, "person_count": number}"""

def encode(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
def ask_openai(image_path):
    client = OpenAI()
    b64 = encode(image_path)
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o", temperature=0,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
        ]}])
    return resp.choices[0].message.content, time.time() - start

from anthropic import Anthropic

def ask_claude(image_path):
    client = Anthropic()
    b64 = encode(image_path)
    start = time.time()
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=100, temperature=0,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": b64}},
            {"type": "text", "text": PROMPT}
        ]}])
    return resp.content[0].text, time.time() - start

from google import genai
from google.genai import types

def ask_gemini(image_path):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    with open(image_path, "rb") as f:
        raw = f.read()
    start = time.time()
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            types.Part.from_bytes(data=raw, mime_type="image/jpeg"),
            PROMPT],
        config=types.GenerateContentConfig(temperature=0))
    return resp.text, time.time() - start

import json

def parse(text):
    clean = text.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1]
        clean = clean.rsplit("```", 1)[0]
    return json.loads(clean)