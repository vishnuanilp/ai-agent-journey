from ultralytics import YOLO

FRAME = r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\street_crowd.jpg"

model = YOLO("yolov8n.pt")
results = model(FRAME)

r = results[0]
print("rows found:", len(r.boxes))
print(r.boxes)