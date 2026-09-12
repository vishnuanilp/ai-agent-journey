# ask_test1.py
from ask1 import ask_url
import builtins

CASES = ["  https://x.com  ", "", "www.x.com", "https://ok.com"]

for c in CASES:
    builtins.input = lambda _prompt="": c
    try:
        print("OK  ", repr(c), "->", repr(ask_url()))
    except ValueError as e:
        print("FAIL", repr(c), "->", type(e).__name__, e)