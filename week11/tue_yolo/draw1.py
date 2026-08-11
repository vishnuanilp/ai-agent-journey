from ultralytics import YOLO
from PIL import Image, ImageDraw

FRAME = r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\street_crowd.jpg"

r = YOLO("yolov8n.pt")(FRAME)[0]
img = Image.open(FRAME)
d = ImageDraw.Draw(img)

for i in range(len(r.boxes)):
    x1, y1, x2, y2 = r.boxes.xyxy[i].tolist()
    c = float(r.boxes.conf[i])
    d.rectangle([x1, y1, x2, y2], outline="red", width=3)
    d.text((x1 + 4, y1 + 4), f"{i+1}  {c:.2f}", fill="red")

img.save("drawn1.png")
print("saved drawn1.png")