from rubric import RUBRIC

SAMPLES = [
    {"q": "Is delivery free?",
     "truth": "Free on orders above 500 rupees, otherwise 40 rupees.",
     "answer": "Yes, delivery is free."},

    {"q": "Are you open on Diwali?",
     "truth": "The document does not mention holidays.",
     "answer": "Yes, we are open 8am to 9pm on Diwali."},

    {"q": "What time do you open?",
     "truth": "8am to 9pm Monday to Saturday. Closed Sunday.",
     "answer": "open 8-9 mon-sat / closed sun"},
]

print(RUBRIC)
for s in SAMPLES:
    print("Q:", s["q"], "\nTRUTH:", s["truth"], "\nBOT:", s["answer"], "\n")