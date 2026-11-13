import sys, contextlib, anyio
with contextlib.redirect_stdout(sys.stderr):     # stdout IS the protocol
    from hybrid import ask                       # gate + Wednesday's run_crew
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vocview-hybrid")

@mcp.tool()
async def ask_vocview(question: str) -> str:
    """Answer a hotel guest question. Private guest details are refused."""
    def run():
        with contextlib.redirect_stdout(sys.stderr):
            print(f"===== Q: {question}", file=sys.stderr)
            return ask(question)
    return await anyio.to_thread.run_sync(run)

if __name__ == "__main__":
    mcp.run(transport="stdio")
