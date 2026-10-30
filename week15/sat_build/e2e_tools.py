import copy, json, rag
from search_agent import SPECS
from ans_prompts import PROMPTS
def rewrite(doc, sys_text, prev, new):
    spec = copy.deepcopy(SPECS); spec[0]["function"]["description"] = doc
    msgs = [{"role": "system", "content": sys_text}, {"role": "user", "content": f"(Guest's previous message: {prev})\n{new}"}]
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, messages=msgs, tools=spec, tool_choice="required")
    return json.loads(r.choices[0].message.tool_calls[0].function.arguments)["query"]
def answer_a2(q):
    hits = rag.retrieve(q, "hotel")
    if not hits:
        return "I don't have that information.", hits
    msg = f"{PROMPTS['A2']}Context:\n" + "\n".join(t for _, t, _ in hits) + f"\n\nQuestion: {q}"
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": msg}])
    return r.choices[0].message.content, hits