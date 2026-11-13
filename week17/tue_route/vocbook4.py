import os, sys, sqlite3
from pathlib import Path
HERE = Path(__file__).resolve().parent
FRI = HERE.parents[1] / "week16" / "fri_crew"
sys.path.insert(0, str(FRI))
os.chdir(FRI)
import redis
from openai import OpenAI
from crewai import Agent, Task, Crew, LLM
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from classify_mem import classify_mem_box
from boxes import chat, error_box, route_intent
from hitl_boxes import route_ok
from room_slots import BState, route_start, route_extract, ask
from room_extract import extract
from room_book import approve, book, cancel
from remember import remember
from hotel_crew import find
from hotel_agents import researcher
from crew3 import crew, analyse, write
from crew3_agents import analyst, writer

find.description = ("Guest asks: {question}\n"
    "Search the hotel documents and copy the policy text about this topic, "
    "even if it says no or sets a limit. "
    "Write NOT FOUND only if no returned text is about the topic.")
find._original_description = None

# HARD crew: same Researcher + find task; Analyst and Writer on Claude Sonnet 5.5
# No temperature: anthropic 2.8.0 messages.create() has no temperature parameter.
SONNET = LLM(model="anthropic/claude-sonnet-5-5")
analyst_h = Agent(role=analyst.role, goal=analyst.goal, backstory=analyst.backstory,
                  llm=SONNET, max_iter=3, verbose=False)
writer_h = Agent(role=writer.role, goal=writer.goal, backstory=writer.backstory,
                 llm=SONNET, max_iter=3, verbose=False)
analyse_h = Task(description=analyse.description, expected_output=analyse.expected_output, agent=analyst_h)
write_h = Task(description=write.description, expected_output=write.expected_output, agent=writer_h)
crew_hard = Crew(agents=[researcher, analyst_h, writer_h], tasks=[find, analyse_h, write_h])

# ROUTER: one cheap call, MISS only. Anything not clearly SIMPLE goes HARD.
OAI = OpenAI()
ROUTER = ("A hotel guest asked: <<Q>>\n"
    "SIMPLE = one fact from the hotel's policy answers it (is there X, opening hours, a price).\n"
    "HARD = it combines several conditions, describes the guest's own situation, or needs reasoning.\n"
    "Reply with one word: SIMPLE or HARD.")

def route_level(q):
    try:
        r = OAI.chat.completions.create(model="gpt-4o-mini", temperature=0, max_tokens=3,
                messages=[{"role": "user", "content": ROUTER.replace("<<Q>>", q)}])
        word = r.choices[0].message.content.strip().upper()
    except Exception:
        word = "ERROR"
    return "simple" if word.startswith("SIMPLE") else "hard"

R = redis.Redis(decode_responses=True)
TTL = 3600

def cache_key(s):
    q = " ".join(str(s["question"]).lower().split())
    return f"vocview:{s.get('business')}:{q}"

def crew_box(s):
    k = cache_key(s)
    try:
        hit = R.get(k)
    except redis.RedisError as e:
        print("  CACHE: READ ERROR", repr(e))
        hit = None
    if hit is not None:
        print("  CACHE: HIT ", k)
        return {"answer": hit}
    print("  CACHE: MISS", k)
    level = route_level(s["question"])
    print("  ROUTE:", level.upper())
    c = crew if level == "simple" else crew_hard
    out = c.kickoff(inputs={"question": s["question"]})
    try:
        R.set(k, out.raw, ex=TTL)
        print("  CACHE: SAVED", k)
    except redis.RedisError as e:
        print("  CACHE: WRITE ERROR", repr(e))
    return {"answer": out.raw}

g = StateGraph(BState)
for n, f in [("classify", classify_mem_box), ("crew", crew_box), ("extract", extract), ("ask",ask),
             ("approve", approve), ("book", book), ("cancel", cancel), ("chat", chat), ("error_box", error_box), ("remember", remember)]:
    g.add_node(n, f)
g.add_conditional_edges(START, route_start, {"extract": "extract", "classify": "classify"})
g.add_conditional_edges("classify", route_intent,
    {"question": "crew", "action": "extract", "chitchat": "chat", "error": "error_box"})
g.add_conditional_edges("extract", route_extract, {"classify": "classify", "ask": "ask", "approve":"approve", "cancel": "cancel"})
g.add_conditional_edges("approve", route_ok, {"book": "book", "cancel": "cancel"})
for n in ["crew", "ask", "book", "cancel", "chat", "error_box"]:
    g.add_edge(n, "remember")
g.add_edge("remember", END)
DB = HERE / "vocbook4.db"
app = g.compile(checkpointer=SqliteSaver(sqlite3.connect(DB, check_same_thread=False)))
