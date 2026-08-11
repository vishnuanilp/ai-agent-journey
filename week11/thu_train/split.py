import os, shutil

names = sorted(f[:-4] for f in os.listdir("images") if f.endswith(".jpg"))
cut = int(len(names) * 0.8)

for part, group in (("train", names[:cut]), ("val", names[cut:])):
    for kind, ext in (("images", ".jpg"), ("labels", ".txt")):
        os.makedirs(f"ds/{part}/{kind}", exist_ok=True)
        for s in group:
            shutil.copy(f"{kind}/{s}{ext}", f"ds/{part}/{kind}/{s}{ext}")
print("train:", cut, " val:", len(names) - cut)