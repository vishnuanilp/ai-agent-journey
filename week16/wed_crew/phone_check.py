from crewai import Agent, Task, Crew
from hotel_agents import llm, researcher
from hotel_tool import TOOL_LOG
from counter import CALLS

caller = Agent(role="Phone tester", llm=llm, max_iter=3, verbose=False, allow_delegation=True,
    goal="Get the hotel's pet policy text from the Hotel policy researcher",
    backstory="You have no search tool. The only way to get hotel policy is to ask the Hotel policy researcher.")
call = Task(description="Use the Delegate work tool. Coworker: Hotel policy researcher. "
    "Task: search the hotel documents for 'can I bring my dog?' and return the exact text found.",
    expected_output="The exact policy text the researcher returned", agent=caller)
crew = Crew(agents=[caller, researcher], tasks=[call], verbose=False)
out = crew.kickoff()
print("SEARCHED:", TOOL_LOG)
print("ANSWER:  ", out.raw.replace("\n", " "))
print("CALLS:   ", len(CALLS))
