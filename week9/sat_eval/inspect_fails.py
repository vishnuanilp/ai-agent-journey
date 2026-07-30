from bot import ask

FAILS = [
    "What time do you open?",
    "Can I pay by phone?",
    "Are you open on Diwali?",
    "Do you sell alcohol?",
    "What is your email address?",
]

for q in FAILS:
    print("Q:", q)
    print("A:", ask(q, k=2))
    print()