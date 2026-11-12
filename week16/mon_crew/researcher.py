from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, LLM

llm = LLM(model="gpt-4o-mini", temperature=0)
researcher = Agent(
    role="Clinic policy researcher",
    goal="Find the exact policy lines that answer the patient's question",
    backstory="You only report lines from the clinic documents you are given.",
    llm=llm, max_iter=3, verbose=False)