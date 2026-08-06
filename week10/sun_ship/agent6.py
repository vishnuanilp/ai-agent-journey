import os, sys, json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from events import get_events

RULES = """You answer questions about a shop's camera event log.
Each record describes ONE frame and nothing else.
person_present true = a person was seen. false = the frame was
checked and was empty. null = NOBODY EVER LOOKED at that frame.
Never use one record as evidence about another frame, whatever
their timestamps. If a frame's person_present is null, the only
honest answer about that frame is that it was not checked.
If the user attaches an image, answer from the image itself and
say so; do not mix it up with the records."""

print("PYTHON:", sys.executable)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
rows = get_events()
history = [types.Content(role="user", parts=[types.Part.from_text(
    text="Camera event records:\n" + json.dumps(rows, indent=1))])]
print("ask a question. end with @filename to attach a frame.")

while True:
    line = input("\nyou: ").strip()
    if line.lower() == "quit":
        break
    q, img = line, ""
    if "@" in line:
        q, img = line.split("@", 1)
        q, img = q.strip(), img.strip()
    parts = [types.Part.from_text(text=q)]
    if img:
        path = os.path.join("frames", img)
        if not os.path.exists(path):
            print("   [no such frame:", img, "] available:", os.listdir("frames"))
            continue
        with open(path, "rb") as f:
            parts.insert(0, types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        print("   [attached", img, "]")
    history.append(types.Content(role="user", parts=parts))
    try:
        resp = client.models.generate_content(
            model="gemini-3.6-flash", contents=history,
            config=types.GenerateContentConfig(system_instruction=RULES))
    except Exception as e:
        print("agent: [no answer — the model could not be reached]")
        print("   ", type(e).__name__, str(e)[:120])
        history.pop()
        continue
    print("agent:", resp.text)
    history.append(types.Content(role="model", parts=[types.Part.from_text(text=resp.text)]))