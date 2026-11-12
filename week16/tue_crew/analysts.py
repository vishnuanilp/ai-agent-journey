from crewai import Agent, LLM

llm = LLM(model="gpt-4o-mini", temperature=0)
ROLE = "Hotel Policy Analyst"
GOAL = "Analyse the research for the guest's question"

vague = Agent(role=ROLE, goal=GOAL, llm=llm, max_iter=3,
    backstory="You are a helpful analyst.")

sharp = Agent(role=ROLE, goal=GOAL, llm=llm, max_iter=3,
    backstory=("You sit between the Researcher and the Writer. You never search "
        "and never write to the guest. Check every detail of the question "
        "against the research text. Output exactly: VERDICT (YES/NO/UNKNOWN), "
        "REASON, LINE USED. If the text does not cover a detail, say UNKNOWN."))