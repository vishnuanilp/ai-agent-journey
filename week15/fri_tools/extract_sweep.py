from salon_extract import client, RULE
from langchain_core.messages import AIMessage, HumanMessage, convert_to_openai_messages
RULE_B = RULE + " A reply of just a day or just a time counts as stating it."
def raw(rule, msgs):
    r = client.chat.completions.create(model="gpt-4o-mini", temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": rule}] + convert_to_openai_messages(msgs))
    return r.choices[0].message.content
CASES = [("Which day would you like?", "Saturday"), ("Which time would you like?", "10am"),
         ("Which day would you like?", "hmm not sure yet")]
for ask, reply in CASES:
    print(f"{reply!r:20} A={raw(RULE, [AIMessage(ask), HumanMessage(reply)])}"
          f"  B={raw(RULE_B, [HumanMessage(reply)])}"
          f"  A+B={raw(RULE_B, [AIMessage(ask), HumanMessage(reply)])}")