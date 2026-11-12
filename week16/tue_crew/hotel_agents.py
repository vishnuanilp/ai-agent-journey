from crewai import Agent, LLM
from hotel_tool import search_hotel_policy

llm = LLM(model="gpt-4o-mini", temperature=0)
researcher = Agent(
    role="Hotel policy researcher",
    goal="Find the exact hotel policy text that answers the guest's question",
    backstory="You always search the hotel documents. You only report what the search returns.",
    tools=[search_hotel_policy], llm=llm, max_iter=3, verbose=False)
responder = Agent(
    role="Hotel front-desk responder",
    goal="Reply to the guest in one or two friendly sentences",
    backstory="You reply only from the research you are handed. You never add facts.",
    llm=llm, max_iter=3, verbose=False)