log = []

def record(user, action, outcome):
    log.append({"user": user, "action": action, "outcome": outcome})

record("asha", "fetch", "ALLOWED")
record("asha", "fetch", "ALLOWED")
record("asha", "fetch", "ALLOWED")
record("asha", "fetch", "REFUSED: daily limit")
record("asha", "fetch", "REFUSED: daily limit")
record("ravi", "fetch", "ALLOWED")

for row in log:
    print(row)