DAILY_LIMIT = 3
counts = {}

def allow(user, today):
    key = (user, today)
    used = counts.get(key, 0)
    if used >= DAILY_LIMIT:
        return False
    counts[key] = used + 1
    return True

for user, day in [("asha","MON"),("asha","MON"),("asha","MON"),
                  ("asha","MON"),("ravi","MON"),("asha","TUE")]:
    print(user, day, "->", "ALLOWED" if allow(user, day) else "REFUSED")

print()
for (u, d), c in counts.items():
    print("row:", u, d, "count =", c)