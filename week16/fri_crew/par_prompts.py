from search_agent import SPECS, SYSTEM
OLD_DOC = "Search the hotel's documents. query = the guest's question as one standalone question."
B3_DOC = SPECS[0]["function"]["description"]
SYS = SYSTEM["content"]
VARIANTS = {"OLD+par": (OLD_DOC, True), "OLD+P1": (OLD_DOC, False),
            "B3+par": (B3_DOC, True), "B3+P1": (B3_DOC, False)}
CASES = [
    ("can I bring my dog?", "what about cats?", "ANSWER"),
    ("is breakfast included?", "what about parking?", "ANSWER"),
    ("do you have a pool?", "what time does it open?", "REFUSE"),
    ("what about cats?", "do you sell phones?", "REFUSE"),
    ("can I bring my dog?", "is breakfast included?", "ANSWER"),
]