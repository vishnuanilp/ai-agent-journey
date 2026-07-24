import sys, time, httpx

name = sys.argv[1]
start = time.time()
first = None

with httpx.stream("GET", "http://127.0.0.1:8000/stream",
                  params={"message": "explain in 150 words how a hotel handles late checkout"},
                  timeout=60) as r:
    for line in r.iter_lines():
        if line.startswith("data:"):
            now = time.time() - start
            if first is None:
                first = now
                print(f"{name} FIRST TOKEN at {now:.2f}s")
            print(f"{name} {now:.2f}")

print(f"{name} DONE at {time.time() - start:.2f}s  (first was {first:.2f}s)")