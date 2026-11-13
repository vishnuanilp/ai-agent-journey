import re
rows = []
for line in open("bench.log", encoding="utf-8"):
    if m := re.search(r"===== Q: (.*)", line): rows.append({"q": m[1].strip(), "route": "?", "cost": 0.0, "http": 0})
    elif rows and "GATE: SENSITIVE" in line: rows[-1]["route"] = "REFUSED"
    elif rows and (m := re.search(r"ROUTE: (\w+)", line)): rows[-1]["route"] = m[1]
    elif rows and (m := re.search(r"COST: \$([\d.]+)", line)): rows[-1]["cost"] = float(m[1])
    elif rows and "HTTP Request" in line: rows[-1]["http"] += 1
for r in rows: print(f"{r['route']:8} {r['http']:3} calls  ${r['cost']:.6f}  {r['q'][:50]}")
total = sum(r["cost"] for r in rows)
hard = [r["cost"] for r in rows if r["route"] == "HARD"]
base = len(rows) * sum(hard) / len(hard) if hard else 0
print(f"TOTAL ${total:.6f}  |  ALL-CLAUDE ESTIMATE ${base:.6f}  |  SAVED {100*(1-total/base):.0f}%" if base else f"TOTAL ${total:.6f}")
