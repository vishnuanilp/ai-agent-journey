import rag

rag.CUTOFF = 99.0

for q in ["Do you accept cards?", "sunday?", "Where do I leave my car?"]:
    hits = rag.retrieve(q, "market", k=3)
    print(q)
    for h in hits:
        print("   ", round(h[2], 3), h[1][:50])
    print()