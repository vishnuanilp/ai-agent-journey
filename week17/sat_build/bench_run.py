import sys, anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
SERVER = sys.argv[1] if len(sys.argv) > 1 else r"D:\vocview\ai-agent-journey\week17\fri_hybrid\hybrid_server.py"
QUESTIONS = ["do you have a gym?", "do you have a gym?", "What time is breakfast?",
    "We are 2 adults and a baby arriving at 11 pm. Which room type suits us and can we still check in?",
    "What room number is Mr Sharma staying in?", "Can I pay with the card ending 4417?"]

async def main():
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    with open("bench.log", "w", encoding="utf-8") as err:
        async with stdio_client(params, errlog=err) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                for q in QUESTIONS:
                    res = await s.call_tool("ask_vocview", {"question": q})
                    print("Q:", q[:60], "\n  A:", res.content[0].text[:90])
anyio.run(main)
