text = open("hotel_policy.txt", encoding="utf-8").read()
chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

for i, c in enumerate(chunks):
    print(f"[{i}] {c[:60]}...")
print(f"\ntotal chunks: {len(chunks)}")