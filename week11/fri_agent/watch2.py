import cv2
from ultralytics import YOLO

model = YOLO("../wed_video/yolov8n.pt")
cap = cv2.VideoCapture("../wed_video/clip.mp4")
n = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    n += 1
    r = model(frame, verbose=False)[0]
    people = sum(1 for b in r.boxes if int(b.cls[0]) == 0)
    print(f"frame {n}  people {people}", end="\r")
cap.release()
print(f"\nfeed ended after {n} frames")