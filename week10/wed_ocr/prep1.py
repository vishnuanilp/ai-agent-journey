from PIL import Image

img = Image.open("frames/clean_text.jpg")
print("colour:", img.mode, img.size)
print("one pixel:", img.getpixel((400, 300)))

grey = img.convert("L")
print("grey:  ", grey.mode, grey.size)
print("one pixel:", grey.getpixel((400, 300)))

grey.save("frames/step1_grey.jpg")
print("saved")