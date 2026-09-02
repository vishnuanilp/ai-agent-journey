verdicts = ["UNSAFE", "UNSAFE.", "unsafe", "The page is UNSAFE.", ""]

for verdict in verdicts:
    if verdict == "UNSAFE":
        result = "BLOCKED"
    else:
        result = "ALLOWED"
    print(repr(verdict), "->", result)