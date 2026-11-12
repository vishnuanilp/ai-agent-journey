import json, rag
from cancel_cases import VARIANTS, CASES
def run(rule, text):
    msg = f"(We asked: How many nights?)\n{text}"
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": rule}, {"role": "user", "content": msg}])
    return json.loads(r.choices[0].message.content)
for name, rule in VARIANTS.items():
    good = 0
    for text, want in CASES:
        outs = [run(rule, text) for _ in range(3)]
        ok = sum(bool(o.get("cancel")) == want for o in outs)
        good += ok
        print(f"  {name} | {ok}/3 | want cancel={want} | {text!r} -> {outs[0]}")
    print(f"{name} TOTAL {good}/30")
