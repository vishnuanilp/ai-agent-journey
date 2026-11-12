from crewai import Task, Crew
from hotel_agents import researcher
from hotel_crew import find
from crew3_agents import analyst, writer

analyse = Task(
    description="Guest asks: {question}\nCheck every detail of the question against the research.",
    expected_output="VERDICT (YES/NO/UNKNOWN), REASON, LINE USED",
    agent=analyst)
write = Task(
    description="Reply to the guest: {question}\nUse only the Analyst's verdict.",
    expected_output="Two or three plain sentences, no greeting or signature",
    agent=writer)
crew = Crew(agents=[researcher, analyst, writer], tasks=[find, analyse, write], verbose=False)
