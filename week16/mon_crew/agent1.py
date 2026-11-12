from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, LLM
from counter import CALLS

llm = LLM(model="gpt-4o-mini", temperature=0)
desk = Agent(
    role="Clinic front-desk assistant",
    goal="Answer the patient's question in one short sentence",
    backstory="You work at a small dental clinic. If you do not know, say so.",
    llm=llm, max_iter=3, verbose=False)
r = desk.kickoff("Can I bring my child to my appointment?")
print("ANSWER:", r.raw)
print("CALLS:", len(CALLS))