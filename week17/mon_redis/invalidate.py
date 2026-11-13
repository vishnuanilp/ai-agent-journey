import sys
import redis

R = redis.Redis(decode_responses=True)
business = sys.argv[1]
keys = list(R.scan_iter(match=f"vocview:{business}:*"))
n = R.delete(*keys) if keys else 0
print(f"INVALIDATED {business}: {n} keys")
for k in keys:
    print("  -", k)
