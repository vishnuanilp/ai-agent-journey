from crewai import Task, Crew, Process
from hotel_agents import researcher, llm
from hotel_crew import find
from crew3 import analyse, write
from crew3_agents import analyst, writer

# same task text as crew3, but NO agent on any task -> the manager picks who does each one
tasks = [Task(description=t.description, expected_output=t.expected_output)
         for t in (find, analyse, write)]
crew = Crew(agents=[researcher, analyst, writer], tasks=tasks,
            process=Process.hierarchical, manager_llm=llm, verbose=False)
