from PIL import ImageFilter
from blur1 import sharpness, small

for name in ["clean_text.jpg", "blurry.jpg", "dark_person.jpg"]:
    img = small("frames/" + name)
    raw = sharpness(img)
    smeared = sharpness(img.filter(ImageFilter.GaussianBlur(3)))
    print(f"{name:18} sharpness {raw:6.2f}   blurred {smeared:5.2f}   ratio {raw/smeared:.1f}")