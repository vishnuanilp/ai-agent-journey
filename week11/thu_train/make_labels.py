import os

line = "0 0.891 0.656 0.219 0.688"
os.makedirs("labels", exist_ok=True)

n = 0
for f in os.listdir("images"):
    if f.endswith(".jpg"):
        stem = os.path.splitext(f)[0]
        with open(os.path.join("labels", stem + ".txt"), "w") as fh:
            fh.write(line + "\n")
        n += 1
print("labels written:", n)