verdicts = ["UNSAFE", "UNSAFE.", "unsafe", "The page is UNSAFE.", ""]

for verdict in verdicts:
    v = verdict.strip().lower()
    blocked = "unsafe" in v
    looks_clean = "safe" in v
    print(repr(verdict), "| blocked:", blocked, "| looks_clean:", looks_clean)