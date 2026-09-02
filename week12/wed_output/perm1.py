ALLOWED = {"summarise": ["speak"], "booking": ["speak", "cancel_booking"]}

def run_tool(job, tool):
    if tool in ALLOWED[job]:
        print(job, "->", tool, ": RUN")
    else:
        print(job, "->", tool, ": DENIED")

run_tool("summarise", "speak")
run_tool("summarise", "cancel_booking")
run_tool("booking", "cancel_booking")