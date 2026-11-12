from crewai import Task, Crew
from hotel_agents import researcher, responder

find = Task(
    description="Guest asks: {question}\nSearch the hotel documents and copy the policy text that answers it.",
    expected_output="The exact policy text copied word for word, or NOT FOUND",
    agent=researcher)
reply = Task(
    description="Reply to the guest: {question}\nIf the research gives a general rule that covers "
                "the guest's case, answer from that rule directly. Only if the research says "
                "NOT FOUND, say you don't have that information.",
    expected_output="One or two friendly sentences",
    agent=responder)
crew = Crew(agents=[researcher, responder], tasks=[find, reply], verbose=False)