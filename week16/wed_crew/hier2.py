from crewai import Task, Crew, Process
from hotel_agents import researcher, llm
from hotel_crew import find
from crew3 import analyse, write
from crew3_agents import analyst, writer

# ONE change from hier.py: each task keeps its crew3 worker -> the manager's phone lists only that worker
tasks = [Task(description=t.description, expected_output=t.expected_output, agent=a)
         for t, a in ((find, researcher), (analyse, analyst), (write, writer))]
crew = Crew(agents=[researcher, analyst, writer], tasks=tasks,
            process=Process.hierarchical, manager_llm=llm, verbose=False)
