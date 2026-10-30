BASE = "Answer the customer's question using ONLY the context below.\n"
END = "If the answer is not in the context, say you don't know.\n\n"
A1 = "If the context gives a rule for a general group, apply it to a specific member of that group.\n"
A2 = ("If the context gives a rule for a general group (e.g. 'children'), apply it to a specific "
      "member (e.g. a 5-year-old). Never stretch a rule to a different topic.\n")
PROMPTS = {"OLD": BASE + END, "A1": BASE + A1 + END, "A2": BASE + A2 + END}
TESTS = [
    ("What is the hotel's policy on bringing cats?", "ANSWER"),
    ("Can I bring my cat to the hotel?", "ANSWER"),
    ("Can I bring my 20kg dog?", "ANSWER"),
    ("Can my cat come on the pool deck?", "ANSWER"),
    ("Is parking free?", "REFUSE"),
    ("Is late check-out available?", "REFUSE"),
]