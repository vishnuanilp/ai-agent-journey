def call_llm(prompt):
    response = expensive_claude_call(prompt)
    return f"Claude says: {response}"

def expensive_claude_call(prompt):
    return "real answer from the internet"