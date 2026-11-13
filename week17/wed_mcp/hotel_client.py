import sys, asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = r"D:\vocview\ai-agent-journey\week17\wed_mcp\hotel_server.py"

async def main():
    p = StdioServerParameters(command=sys.executable, args=[SERVER],
                              env={"PYTHONIOENCODING": "utf-8"})
    with open("server_err.log", "w", encoding="utf-8") as log:
        async with stdio_client(p, errlog=log) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                tools = await s.list_tools()
                print("TOOLS:", [t.name for t in tools.tools])
                for q in sys.argv[1:]:
                    res = await s.call_tool("ask_hotel", {"question": q})
                    print("Q:", q)
                    print("  ANSWER:", res.content[0].text.replace("\n", " "))

asyncio.run(main())
