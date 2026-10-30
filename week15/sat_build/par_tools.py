import copy, json, rag
from search_agent import SPECS
def rewrite_all(doc, sys_text, prev, new, parallel):
    spec = copy.deepcopy(SPECS); spec[0]["function"]["description"] = doc
    msgs = [{"role": "system", "content": sys_text}, {"role": "user", "content": f"(Guest's previous message: {prev})\n{new}"}]
    extra = {} if parallel else {"parallel_tool_calls": False}
    r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, messages=msgs, tools=spec, tool_choice="required", **extra)
    return [json.loads(c.function.arguments)["query"] for c in r.choices[0].message.tool_calls]