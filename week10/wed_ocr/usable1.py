from PIL import Image

FRAMES = ["clean_text.jpg", "dark_person.jpg", "blurry.jpg"]

for name in FRAMES:
    grey = Image.open(f"frames/{name}").convert("L")
    pixels = list(grey.getdata())
    n = len(pixels)
    mean = sum(pixels) / n
    spread = sum(abs(p - mean) for p in pixels) / n
    print(f"{name:<18} pixels {n:>9}  mean {mean:6.1f}  spread {spread:6.1f}")