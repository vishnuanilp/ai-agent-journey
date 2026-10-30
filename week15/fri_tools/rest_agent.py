import json
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.messages import AIMessage, convert_to_openai_messages
from langchain_core.utils.function_calling import convert_to_openai_tool
from rest_tools import TOOLS
load_dotenv()
client = OpenAI()
SPECS = [convert_to_openai_tool(t) for t in TOOLS]
SYSTEM = {"role": "system", "content": "You help guests of a small restaurant. Use the tools; never guess."}
def agent(state):
    msgs = [SYSTEM] + convert_to_openai_messages(state["messages"])
    r = client.chat.completions.create(model="gpt-4o-mini", temperature=0, messages=msgs, tools=SPECS).choices[0].message
    calls = [{"name": c.function.name, "args": json.loads(c.function.arguments), "id": c.id} for c in (r.tool_calls or [])]
    return {"messages": [AIMessage(content=r.content or "", tool_calls=calls)]}