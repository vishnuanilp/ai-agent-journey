from ultralytics import YOLO

FRAMES = [
    r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\street_crowd.jpg",
    r"D:\vocview\ai-agent-journey\week10\mon_vision\frames\room_person.jpg",
]
TRUTH = {"street_crowd.jpg": 9, "room_person.jpg": 2}
model = YOLO("yolov8n.pt")

for path in FRAMES:
    r = model(path, verbose=False)[0]
    confs = [float(r.boxes.conf[i]) for i in range(len(r.boxes))
             if model.names[int(r.boxes.cls[i])] == "person"]
    name = path.split("\\")[-1]
    print(f"\n{name}  (truth {TRUTH[name]})")
    for t in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        kept = len([c for c in confs if c >= t])
        print(f"  thresh {t:.1f} -> {kept}   {'OK' if kept == TRUTH[name] else ''}")