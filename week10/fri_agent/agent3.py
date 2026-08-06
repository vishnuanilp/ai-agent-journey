import os, sys, json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from events import get_events

print("PYTHON:", sys.executable)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
rows = get_events()
print("rows loaded:", len(rows))
history = [types.Content(role="user", parts=[types.Part.from_text(
    text="Here are today's camera event records:\n" + json.dumps(rows, indent=1))])]

while True:
    q = input("\nyou: ")
    if q.strip().lower() == "quit":
        break
    history.append(types.Content(role="user", parts=[types.Part.from_text(text=q)]))
    resp = client.models.generate_content(model="gemini-3.6-flash", contents=history)
    print("agent:", resp.text)
    history.append(types.Content(role="model", parts=[types.Part.from_text(text=resp.text)]))