import copy, json, rag
from search_agent import SPECS
from agent_prompts import VARIANTS, CASES
def rewrite(doc, sys_text, prev, new):
    spec = copy.deepcopy(SPECS); spec[0]["function"]["description"] = doc
    msgs = [{"role": "system", "content": sys_text}, {"role": "user", "content": f"(Guest's previous message: {prev})\n{new}"}]
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, messages=msgs, tools=spec, tool_choice="required")
    return json.loads(r.choices[0].message.tool_calls[0].function.arguments)["query"]
for name, (doc, sys_text) in VARIANTS.items():
    good = 0
    for prev, new, topic in CASES:
        qs = [rewrite(doc, sys_text, prev, new) for _ in range(5)]
        ok = [q for q in qs if topic in q.lower() and "policy" not in q.lower()]
        good += len(ok)
        print(f"  {name} | {len(ok)}/5 | {new} -> {sorted(set(qs))}")
    print(f"{name} TOTAL {good}/15")