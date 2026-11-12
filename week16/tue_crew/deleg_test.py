from crewai import Task, Crew
from deleg_agents import researcher, writer
from hotel_tool import TOOL_LOG
from counter import CALLS

for q in ["can I bring my cat?", "do you have a gym?"]:
    print(f"Q: {q}")
    for name, on in [("OFF", False), ("ON", True)]:
        w, c, s = writer(on), len(CALLS), len(TOOL_LOG)
        t = Task(description=f"Guest question: {q}\nResearcher's notes: NOT FOUND",
                 expected_output="The reply to the guest", agent=w)
        out = Crew(agents=[researcher, w], tasks=[t]).kickoff()
        print(f"  {name}: CALLS {len(CALLS)-c} | WORKERS SHOWN {len(out.tasks_output)} | "
              f"SEARCHED {TOOL_LOG[s:]} | REPLY: " + out.raw.replace("\n", " "))