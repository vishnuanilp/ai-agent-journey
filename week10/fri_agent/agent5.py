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
honest answer about that frame is that it was not checked."""

print("PYTHON:", sys.executable)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
rows = get_events()
history = [types.Content(role="user", parts=[types.Part.from_text(
    text="Camera event records:\n" + json.dumps(rows, indent=1))])]

while True:
    q = input("\nyou: ")
    if q.strip().lower() == "quit":
        break
    history.append(types.Content(role="user", parts=[types.Part.from_text(text=q)]))
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