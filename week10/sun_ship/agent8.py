import os, sys, json, base64
from dotenv import load_dotenv
from openai import OpenAI
from events import get_events

RULES = """You answer questions about a shop's camera event log.
Each record describes ONE frame and nothing else.
person_present true = a person was seen. false = the frame was
checked and was empty. null = NOBODY EVER LOOKED at that frame.
Never use one record as evidence about another frame, whatever
their timestamps. If a frame's person_present is null, the only
honest answer about that frame is that it was not checked.
If the user attaches an image, answer from the image itself and
say so; do not mix it up with the records.
The records block is re-read from the database fresh on every
turn and may have grown since your last answer. Never rely on
your own earlier answer for a count or a list — recount from
the records given in this turn, every time."""

print("PYTHON:", sys.executable)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
history = []
print("ask a question. end with @filename to attach a frame.")

while True:
    line = input("\nyou: ").strip()
    if line.lower() == "quit":
        break
    q, img = line, ""
    if "@" in line:
        q, img = line.split("@", 1)
        q, img = q.strip(), img.strip()
    parts = [{"type": "text", "text": q}]
    if img:
        path = os.path.join("frames", img)
        if not os.path.exists(path):
            print("   [no such frame:", img, "] available:", os.listdir("frames"))
            continue
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        parts.append({"type": "image_url",
                      "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
        print("   [attached", img, "]")
    history.append({"role": "user", "content": parts})
    rows = get_events()
    print("   [rows now:", len(rows), "]")
    messages = ([{"role": "system", "content": RULES},
                 {"role": "user", "content": "Camera event records:\n" + json.dumps(rows, indent=1)}]
                + history)
    try:
        resp = client.chat.completions.create(model="gpt-4o", messages=messages)
    except Exception as e:
        print("agent: [no answer — the model could not be reached]")
        print("   ", type(e).__name__, str(e))
        history.pop()
        continue
    answer = resp.choices[0].message.content
    print("agent:", answer)
    history.append({"role": "assistant", "content": answer})