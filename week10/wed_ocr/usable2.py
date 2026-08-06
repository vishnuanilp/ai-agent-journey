from PIL import Image

FRAMES = ["clean_text.jpg", "dark_person.jpg", "blurry.jpg"]
DARK = 40

for name in FRAMES:
    grey = Image.open(f"frames/{name}").convert("L")
    hist = grey.histogram()
    total = sum(hist)
    crushed = sum(hist[:DARK]) / total
    blown = sum(hist[240:]) / total
    print(f"{name:<18} crushed {crushed:6.1%}   blown {blown:6.1%}")