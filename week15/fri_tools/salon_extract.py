import json
from dotenv import load_dotenv
from openai import OpenAI
from salon_slots import FIELDS
load_dotenv()
client = OpenAI()
RULE = ("Return JSON with ONLY the fields the guest's message states: service (haircut, "
        "facial or manicure), day (e.g. Saturday), time (24-hour HH:MM). Leave out the rest. "
        "A reply of just a day or just a time counts as stating it.")
def extract(state):
    r = client.chat.completions.create(model="gpt-4o-mini", temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": RULE}, {"role": "user", "content": state["messages"][-1].content}])
    found = json.loads(r.choices[0].message.content)
    return {k: found[k] for k in FIELDS if found.get(k)}