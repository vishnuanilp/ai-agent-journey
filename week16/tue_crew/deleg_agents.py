from crewai import Agent, LLM
from hotel_tool import search_hotel_policy

llm = LLM(model="gpt-4o-mini", temperature=0)
researcher = Agent(role="Hotel Policy Researcher", llm=llm, max_iter=3,
    goal="Find the exact hotel policy text for a question",
    backstory="You search the hotel's policies and report the exact text, or NOT FOUND.",
    tools=[search_hotel_policy])

def writer(delegate):
    return Agent(role="Hotel Guest Writer", llm=llm, max_iter=3,
        allow_delegation=delegate,
        goal="A short, polite reply to the guest that matches the notes",
        backstory="You write the final reply to the hotel guest from the notes you are handed.")
