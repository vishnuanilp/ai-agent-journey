from dotenv import load_dotenv
from openai import OpenAI
from runners import encode, PROMPT

load_dotenv()
client = OpenAI()
b64 = encode("frames/room_person.jpg")
resp = client.chat.completions.create(
    model="gpt-4o", temperature=0,
    messages=[{"role": "user", "content": [
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
    ]}])
print(resp.usage)