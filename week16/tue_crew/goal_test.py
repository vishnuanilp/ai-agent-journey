import sys
from crewai import Task, Crew
from goals import vague_goal, clear_goal

RESEARCH = ("Guests may bring pets. They must be under 10kg and are not "
            "allowed in the dining area or the pool deck.")

for q in sys.argv[1:]:
    print(f"Q: {q}")
    for name, agent in [("VAGUE_GOAL", vague_goal), ("CLEAR_GOAL", clear_goal)]:
        t = Task(description=f"Guest question: {q}\nResearch text: {RESEARCH}",
                 expected_output="Your analysis", agent=agent)
        out = Crew(agents=[agent], tasks=[t]).kickoff()
        print(f"  {name}: " + out.raw.replace("\n", " | "))