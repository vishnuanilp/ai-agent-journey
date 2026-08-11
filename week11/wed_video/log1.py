import cv2, csv
from datetime import datetime
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("clip.mp4")
f = open("log.csv", "w", newline="", encoding="utf-8")
w = csv.writer(f)
w.writerow(["frame", "video_s", "wall_clock", "people"])

i = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    r = model(frame, verbose=False)[0]
    n = sum(1 for b in r.boxes if int(b.cls) == 0)
    w.writerow([i, round(i / 11, 2), datetime.now().isoformat(timespec="seconds"), n])
    i += 1

f.close()
cap.release()