from PIL import Image, ImageFilter

def sharpness(img):
    px = img.load()
    w, h = img.size
    total = 0
    for y in range(h):
        for x in range(w - 1):
            total += abs(px[x, y] - px[x + 1, y])
    return total / ((w - 1) * h)

def small(path):
    im = Image.open(path).convert("L")
    return im.resize((800, int(800 * im.height / im.width)))

clean = small("frames/clean_text.jpg")
print("clean        ", round(sharpness(clean), 2))
print("blurred by 3 ", round(sharpness(clean.filter(ImageFilter.GaussianBlur(3))), 2))