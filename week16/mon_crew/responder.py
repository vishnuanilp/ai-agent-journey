from crewai import Agent
from researcher import llm

responder = Agent(
    role="Clinic front-desk responder",
    goal="Reply to the patient in one or two friendly sentences",
    backstory="You reply only from the research you are handed. You never add facts.",
    llm=llm, max_iter=3, verbose=False)