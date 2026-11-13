import sys, json, asyncio
from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv(r"D:\vocview\ai-agent-journey\week16\fri_crew\.env")
SERVER = r"D:\vocview\ai-agent-journey\week17\wed_mcp\hotel_server.py"
MODEL = "gpt-4o-mini"
ROLE = sys.argv[1]                  # guest | operator
llm = OpenAI()

def price(u):                       # gpt-4o-mini $0.15 in / $0.60 out per 1M
    return (u.prompt_tokens * 0.15 + u.completion_tokens * 0.60) / 1e6

async def ask(s, tools, q):
    msgs = [{"role": "user", "content": q}]
    cost, used = 0.0, 0
    print("Q:", q)
    for _ in range(4):                  # max 4 rounds: stops a runaway tool loop
        r = llm.chat.completions.create(model=MODEL, messages=msgs, tools=tools, temperature=0)
        cost += price(r.usage)
        m = r.choices[0].message
        if not m.tool_calls:
            break
        msgs.append(m.model_dump(exclude_none=True))
        for tc in m.tool_calls:
            args = json.loads(tc.function.arguments)
            print("  TOOL:", tc.function.name, args)
            res = await s.call_tool(tc.function.name, args)
            print("  RESULT:", res.content[0].text.replace("\n", " "))
            msgs.append({"role": "tool", "tool_call_id": tc.id, "content": res.content[0].text})
            used += 1
    else:
        print("  STOPPED: 4 rounds, no final answer")
    if used == 0:
        print("  TOOL: none")
    print("  ANSWER:", (m.content or "(no text)").replace("\n", " "))
    print(f"  CLIENT COST: ${cost:.6f}")

async def main():
    p = StdioServerParameters(command=sys.executable, args=[SERVER, ROLE],
                              env={"PYTHONIOENCODING": "utf-8"})
    with open("server_err.log", "w", encoding="utf-8") as log:
        async with stdio_client(p, errlog=log) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                listed = await s.list_tools()
                tools = [{"type": "function", "function": {"name": t.name,
                          "description": t.description, "parameters": t.inputSchema}}
                         for t in listed.tools]
                print("ROLE:", ROLE, " MENU:", [t["function"]["name"] for t in tools])
                for q in sys.argv[2:]:
                    await ask(s, tools, q)

asyncio.run(main())
