CAPACITY = 3
tokens = CAPACITY

def allow():
    global tokens
    if tokens > 0:
        tokens -= 1
        return True
    return False

requests = ["cut", "colour", "beard", "facial", "wash"]
for r in requests:
    print(r, "->", "ALLOWED" if allow() else "REFUSED", "| tokens left:", tokens)