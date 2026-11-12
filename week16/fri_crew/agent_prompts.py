from search_agent import SYSTEM, SPECS
OLD_DOC = SPECS[0]["function"]["description"]
NEW_DOC = ("Search the hotel's documents. query = the guest's question as one standalone question, "
           "in the guest's own voice (e.g. 'Can I check in early?', 'What time does breakfast start?'). "
           "Never turn it into a question about a 'policy'.")
OLD_SYS = SYSTEM["content"]
NEW_SYS = OLD_SYS + " Keep the guest's own wording; only add what the earlier message supplies."
VARIANTS = {"OLD": (OLD_DOC, OLD_SYS), "B1": (NEW_DOC, OLD_SYS), "B2": (NEW_DOC, NEW_SYS)}
CASES = [
    ("can I bring my dog?", "what about cats?", "cat"),
    ("is breakfast included?", "what about parking?", "park"),
    ("do you have a pool?", "what time does it open?", "pool"),
]