import base64, os, mimetypes
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask(path):
    mime = mimetypes.guess_type(path)[0]
    raw = Path(path).read_bytes()
    url = f"data:{mime};base64,{base64.b64encode(raw).decode('utf-8')}"
    resp = client.chat.completions.create(model="gpt-4o", temperature=0,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Reply with one word: what room is this?"},
            {"type": "image_url", "image_url": {"url": url}}]}])
    return mime, resp.choices[0].message.content

for f in ["frames/room_person.jpg", "frames/room_person.png",
          "frames/room_person.tiff", "frames/fake.jpg"]:
    try:
        print(f, "->", ask(f))
    except Exception as e:
        print(f, "-> FAILED:", type(e).__name__, str(e)[:90])