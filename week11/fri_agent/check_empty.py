import cv2
from ultralytics import YOLO

model = YOLO("../wed_video/yolov8n.pt")
cap = cv2.VideoCapture("empty.mp4")
n = 0
hits = []
while True:
    ok, frame = cap.read()
    if not ok:
        break
    n += 1
    r = model(frame, verbose=False)[0]
    confs = [float(b.conf[0]) for b in r.boxes if int(b.cls[0]) == 0]
    if confs:
        hits.append((n, confs))
cap.release()
print(f"{n} frames, {len(hits)} with a person")
print(hits[:10])