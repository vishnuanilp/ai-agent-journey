import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("clip.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)

i = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    r = model(frame, verbose=False)[0]
    people = sum(1 for b in r.boxes if int(b.cls) == 0)
    print(f"{i:4d}  {i/fps:6.2f}s  people={people}")
    i += 1

cap.release()
print("frames processed:", i)