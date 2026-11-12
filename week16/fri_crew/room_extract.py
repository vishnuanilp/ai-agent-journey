import json, rag
from room_slots import FIELDS
RULE = ("Return JSON with ONLY the fields the guest states: day (check-in day, e.g. Saturday), "
        "nights (a number), guests (a number). Leave out the rest. "
        "A reply of just a number answers the question we asked. "
        'If the guest wants to stop or drop the booking, add "cancel": true. Changing a detail is NOT cancelling.')
def extract(s):
    msgs = s["messages"]; text = msgs[-1].content
    if s.get("booking") and len(msgs) > 1 and msgs[-2].type == "ai":
        text = f"(We asked: {msgs[-2].content})\n{text}"
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": RULE}, {"role": "user", "content": text}])
    found = json.loads(r.choices[0].message.content)
    new = {k: str(found[k]) for k in FIELDS if found.get(k)}
    return {**new, "found": len(new), "stop": bool(found.get("cancel")), "booking": "open"}