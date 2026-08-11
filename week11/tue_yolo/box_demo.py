from PIL import Image, ImageDraw

img = Image.new("RGB", (400, 300), "white")
d = ImageDraw.Draw(img)

d.rectangle([0, 0, 399, 299], outline="black")
d.text((5, 5), "(0,0) top-left", fill="black")

d.rectangle([150, 40, 250, 260], outline="red", width=3)
d.text((155, 20), "x1,y1 = 150,40", fill="red")
d.text((155, 265), "x2,y2 = 250,260", fill="red")

img.save("box_demo.png")
print("saved box_demo.png")