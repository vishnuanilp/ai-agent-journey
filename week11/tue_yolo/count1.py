from ultralytics import YOLO

FRAME = r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\street_crowd.jpg"

model = YOLO("yolov8n.pt")
r = model(FRAME)[0]

people = 0
for i in range(len(r.boxes)):
    cls_num = int(r.boxes.cls[i])
    name = model.names[cls_num]
    print(f"row {i+1}: class {cls_num} = {name}")
    if name == "person":
        people += 1

print("total rows:", len(r.boxes))
print("people:", people)