import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("clip.mp4")

i = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    r = model(frame, verbose=False)[0]
    confs = [round(float(b.conf), 2) for b in r.boxes if int(b.cls) == 0]
    print(f"{i:4d} {i/11:6.2f}s n={len(confs)} confs={confs}")
    if i % 10 == 0:
        cv2.imwrite(f"shots/f{i:03d}.jpg", r.plot())
    i += 1
cap.release()