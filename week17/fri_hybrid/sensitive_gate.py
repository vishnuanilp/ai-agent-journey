import re
WORDS = ["phone", "allergy", "passport", "room number", "address", "paid"]
MASKS = [(r"ending\s*\d{4}", "ending ****"), (r"\+?\d[\d\s\-]{7,}\d", "[PHONE]")]

def is_sensitive(q):                       # asks ABOUT private data -> refuse
    return any(w in q.lower() for w in WORDS)

def redact(q):                             # only CONTAINS a number -> mask it
    for pat, rep in MASKS: q = re.sub(pat, rep, q, flags=re.I)
    return q

if __name__ == "__main__":
    for q in ["What's Priya's phone number?", "Note her allergy to henna",
              "What room number is Mr Sharma staying in?", "Do you have a gym?",
              "Can I pay with the card ending 4417?", "Call me on 06 12 34 56 78"]:
        print("REFUSE" if is_sensitive(q) else "SEND  ", "|", redact(q))
