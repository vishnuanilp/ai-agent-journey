verdicts = ["UNSAFE", "unsafe", "safe", "The page is UNSAFE.", ""]

for verdict in verdicts:
    v = verdict.strip().lower()
    if v == "unsafe":
        print(repr(verdict), "-> BLOCK")
    elif v == "safe":
        print(repr(verdict), "-> ALLOW")
    else:
        print(repr(verdict), "-> INVALID, stop")