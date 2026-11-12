from crewai import Task, Crew
from writers import plain, armed
from hotel_tool import TOOL_LOG
from counter import CALLS

PET = "Guests may bring pets. They must be under 10kg and are not allowed in the dining area or the pool deck."
NOTES = {"can I bring my cat?": PET, "do you have a gym?": "NOT FOUND"}

for q, notes in NOTES.items():
    print(f"Q: {q}")
    for name, w in [("PLAIN", plain), ("ARMED", armed)]:
        c, s = len(CALLS), len(TOOL_LOG)
        t = Task(description=f"Guest question: {q}\nResearcher's notes: {notes}",
                 expected_output="The reply to the guest", agent=w)
        out = Crew(agents=[w], tasks=[t]).kickoff()
        print(f"  {name}: CALLS {len(CALLS)-c} | SEARCHED {TOOL_LOG[s:]} | REPLY: " + out.raw.replace("\n", " "))