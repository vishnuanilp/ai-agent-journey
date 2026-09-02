ALLOWED = {"summarise": ["speak", "lookup_rate"], "booking": ["speak", "cancel_booking"]}
RISKY = ["cancel_booking"]

def run_tool(job, tool, confirmed=False):
    if tool not in ALLOWED[job]:
        print(job, "->", tool, ": DENIED")
    elif tool in RISKY and not confirmed:
        print(job, "->", tool, ": NEEDS HUMAN OK")
    else:
        print(job, "->", tool, ": RUN")

run_tool("summarise", "lookup_rate")
run_tool("summarise", "cancel_booking")
run_tool("booking", "cancel_booking")
run_tool("booking", "cancel_booking", confirmed=True)