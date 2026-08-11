from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont

FRAME = r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\street_crowd.jpg"
font = ImageFont.truetype("arial.ttf", 34)

r = YOLO("yolov8n.pt")(FRAME)[0]
img = Image.open(FRAME)
d = ImageDraw.Draw(img)

for i in range(len(r.boxes)):
    x1, y1, x2, y2 = r.boxes.xyxy[i].tolist()
    c = float(r.boxes.conf[i])
    d.rectangle([x1, y1, x2, y2], outline="red", width=3)
    d.rectangle([x1, y1 - 38, x1 + 130, y1], fill="red")
    d.text((x1 + 5, y1 - 36), f"{i+1}: {c:.2f}", fill="white", font=font)
    print(f"row {i+1}: conf {c:.2f}  box {int(x1)},{int(y1)} to {int(x2)},{int(y2)}")

img.save("drawn2.png")
print("saved drawn2.png")