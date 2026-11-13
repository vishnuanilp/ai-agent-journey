import sys
QUESTIONS = sys.argv[1:]                    # save our questions first
sys.argv = [sys.argv[0], "guest"]           # hotel_server reads its ROLE from here
from sensitive_gate import is_sensitive, redact
sys.path.insert(0, r"D:\vocview\ai-agent-journey\week17\wed_mcp")
from hotel_server import run_crew

REFUSAL = "Sorry, I can't share private guest details. Please ask the front desk."

def ask(q):
    if is_sensitive(q):
        print("GATE: SENSITIVE -> REFUSED on PC, 0 cloud calls", file=sys.stderr)
        return REFUSAL
    clean = redact(q)                       # digits masked on the PC
    print("GATE: REDACTED -> cloud" if clean != q else "GATE: SAFE -> cloud", file=sys.stderr)
    return run_crew(clean)

if __name__ == "__main__":
    for q in QUESTIONS:
        print(f"===== Q: {q}", file=sys.stderr)
        print("ANSWER:", ask(q), file=sys.stderr)
