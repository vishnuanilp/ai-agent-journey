import base64, os, json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """Look at this CCTV frame. Reply with ONLY this JSON, nothing else:
{"person_present": true/false, "person_count": 0, "description": "one short sentence"}"""

raw = Path("frames/street_crowd.jpg").read_bytes()
data_url = f"data:image/jpeg;base64,{base64.b64encode(raw).decode('utf-8')}"

resp = client.chat.completions.create(
    model="gpt-4o", temperature=0,
    messages=[{"role": "user", "content": [
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": data_url}},
    ]}],
)
data = json.loads(resp.choices[0].message.content)
print(type(data))

if data["person_present"]:
    print("ALERT — someone in the shop. Count:", data["person_count"])
else:
    print("clear")