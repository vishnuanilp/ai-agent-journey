import sys, uuid, contextlib
import anyio
sys.path.insert(0, r"D:\vocview\ai-agent-journey\week17\tue_route")
with contextlib.redirect_stdout(sys.stderr):
    from langchain_core.messages import HumanMessage
    from vocbook4 import app, R, cache_key   # vocbook4 chdirs to fri_crew
    import redis
    import counter3
from mcp.server.fastmcp import FastMCP

RESET = {"intent": None, "hits": [], "error": None, "answer": None, "ok": None}
mcp = FastMCP("vocview-hotel")

async def ask_hotel(question: str) -> str:
    """Answer a guest's question about the hotel: rooms, facilities, policies. Read-only."""
    return await anyio.to_thread.run_sync(run_crew, question)

def run_crew(question: str) -> str:
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 10}
    n = len(counter3.ROWS)
    with contextlib.redirect_stdout(sys.stderr):
        app.invoke({"question": question, "business": "hotel",
                    "messages": [HumanMessage(question)], **RESET}, cfg)
        rows = counter3.ROWS[n:]
        cost = sum(r["cost"] for r in rows if r["cost"] is not None)
        print(f"COST: ${cost:.6f}  calls {len(rows)}")
    return str(app.get_state(cfg).values.get("answer"))

def cache_status(question: str) -> str:
    """Check if a hotel guest question is already in Vocview's answer cache. Read-only, no AI cost."""
    k = cache_key({"question": question, "business": "hotel"})
    try:
        t = R.ttl(k)
    except redis.RedisError:
        return f"UNKNOWN (redis error) key={k}"
    if t == -2:
        return f"NOT CACHED key={k}"
    return f"CACHED expires_in={t}s key={k}"

ROLE = sys.argv[1] if len(sys.argv) > 1 else "guest"
MENUS = {"guest": [ask_hotel], "operator": [ask_hotel, cache_status]}
for fn in MENUS[ROLE]:              # unknown role -> KeyError, server refuses to start
    mcp.add_tool(fn)

if __name__ == "__main__":
    mcp.run(transport="stdio")
