from ultralytics import YOLO

model = YOLO(r"D:\vocview\ai-agent-journey\runs\detect\runs\door1\weights\best.pt")

paths = [
    r"images\f000.jpg",
    r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\street_crowd.jpg",
]

for path in paths:
    r = model(path, verbose=False)[0]
    print(path, "->", len(r.boxes), "boxes", r.boxes.conf.tolist())