from PIL import Image

def small(path):
    im = Image.open(path).convert("L")
    return im.resize((800, int(800 * im.height / im.width)))

def sharpness(path):
    img = small(path)
    px = img.load()
    w, h = img.size
    total = 0
    for y in range(h):
        for x in range(w - 1):
            total += abs(px[x, y] - px[x + 1, y])
    return total / ((w - 1) * h)