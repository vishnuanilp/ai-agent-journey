from adapter import call_llm

LADDER = [ "claude", "openai", "gemini"]

def route(prompt):
    for provider in LADDER:
        try:
            answer = call_llm(prompt, provider)
            return answer
        except Exception as e:
            print(f"{provider} failed: {e} — falling back")
    raise RuntimeError("All providers failed")

if __name__ == "__main__":
    print(route("Say hello in one short sentence."))