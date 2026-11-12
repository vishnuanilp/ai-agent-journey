from crewai import Agent, LLM
from hotel_tool import search_hotel_policy

llm = LLM(model="gpt-4o-mini", temperature=0)
SETUP = dict(role="Hotel Guest Writer", llm=llm, max_iter=3,
    goal="A short, polite reply to the guest that matches the notes",
    backstory="You write the final reply to the hotel guest from the notes you are handed.")

plain = Agent(**SETUP)
armed = Agent(**SETUP, tools=[search_hotel_policy])