from recursive_split import split_recursive

text = open("hotel_policy.txt", encoding="utf-8").read()
chunks = split_recursive(text, ["\n\n", "\n", ". "], 300)

for i, c in enumerate(chunks):
    print(i, repr(c[:70]))
print("total chunks:", len(chunks))