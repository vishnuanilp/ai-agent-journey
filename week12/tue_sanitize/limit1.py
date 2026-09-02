LIMIT = 5000

pages = [
    ("short review", "Best biryani in Kochi. The dosa was excellent." ),
    ("long article", "The clinic expanded its cardiology wing. " * 400),
]

for name, page in pages:
    n = len(page)
    kept = page[:LIMIT]
    lost = n - len(kept)
    print(f"{name:13} | chars {n:6} | kept {len(kept):5} | lost {lost:6}")