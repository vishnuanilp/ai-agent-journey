import sys
from crewai import Task, Crew
from analysts import vague, sharp

RESEARCH = ("Guests may bring pets. They must be under 10kg and are not "
            "allowed in the dining area or the pool deck.")

for q in sys.argv[1:]:
    print(f"Q: {q}")
    for name, agent in [("VAGUE", vague), ("SHARP", sharp)]:
        t = Task(description=f"Guest question: {q}\nResearch text: {RESEARCH}",
                 expected_output="Your analysis", agent=agent)
        out = Crew(agents=[agent], tasks=[t]).kickoff()
        print(f"  {name}: " + out.raw.replace("\n", " | "))