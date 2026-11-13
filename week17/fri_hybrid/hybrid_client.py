import sys, anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main(questions):
    params = StdioServerParameters(command=sys.executable, args=["hybrid_server.py"])
    with open("hybrid_err.log", "w", encoding="utf-8") as err:
        async with stdio_client(params, errlog=err) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                print("TOOLS:", [t.name for t in (await s.list_tools()).tools])
                for q in questions:
                    res = await s.call_tool("ask_vocview", {"question": q})
                    print("Q:", q, "\n  ANSWER:", res.content[0].text)

anyio.run(main, sys.argv[1:])
