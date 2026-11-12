from crewai import Agent, LLM

llm = LLM(model="gpt-4o-mini", temperature=0)
ROLE = "Hotel Policy Analyst"
BACKSTORY = "You are a helpful analyst."

vague_goal = Agent(role=ROLE, backstory=BACKSTORY, llm=llm, max_iter=3,
    goal="Analyse the research for the guest's question")

clear_goal = Agent(role=ROLE, backstory=BACKSTORY, llm=llm, max_iter=3,
    goal=("Give a YES, NO or UNKNOWN verdict for the guest's exact "
          "question, using only the research notes"))