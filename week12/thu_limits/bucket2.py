import time

CAPACITY = 3
REFILL_PER_SECOND = 1.0

tokens = float(CAPACITY)
last = time.time()

def allow():
    global tokens, last
    now = time.time()
    tokens = min(CAPACITY, tokens + (now - last) * REFILL_PER_SECOND)
    last = now
    if tokens >= 1:
        tokens -= 1
        return True
    return False


for i in range(5):
    print("burst", i + 1, "->", "ALLOWED" if allow() else "REFUSED", "| tokens: %.2f" % tokens)

print("...sleeping 10 seconds...")
time.sleep(10)

for i in range(3):
    print("after wait", i + 1, "->", "ALLOWED" if allow() else "REFUSED", "| tokens: %.2f" % tokens)