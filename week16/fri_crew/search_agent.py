import json
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
import rag
@tool
def hotel_search(query: str) -> str:
    """Search the hotel's documents. query = the guest's question as one standalone question. Example: previous message 'can I bring my bike?', new message 'what about scooters?' -> query 'Can I bring my scooter to the hotel?'"""
SPECS = [convert_to_openai_tool(hotel_search)]
SYSTEM = {"role": "system", "content": "You find hotel information. Always call hotel_search. If the latest question already stands alone, pass it unchanged; if it refers to earlier messages, rewrite it to stand alone."}
def search_agent(s):
    guests = [m.content for m in s["messages"] if m.type == "human"]
    if len(guests) == 1:
        calls = [{"name": "hotel_search", "args": {"query": guests[0]}, "id": "call_first_turn"}]
    else:
        ctx = {"role": "user", "content": f"(Guest's previous message: {guests[-2]})\n{guests[-1]}"}
        r = rag.oa.chat.completions.create(model="gpt-4o-mini", temperature=0, messages=[SYSTEM, ctx], tools=SPECS, tool_choice="required", parallel_tool_calls=False).choices[0].message
        calls = [{"name": c.function.name, "args": json.loads(c.function.arguments), "id": c.id} for c in r.tool_calls]
    return {"messages": [AIMessage(content="", tool_calls=calls)]}