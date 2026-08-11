import cv2, time
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("clip.mp4")
times = []

while True:
    ok, frame = cap.read()
    if not ok:
        break
    t = time.time()
    model(frame, verbose=False)
    times.append(time.time() - t)

cap.release()
rest = times[1:]
print("first call:", round(times[0], 3), "s")
print("rest avg  :", round(sum(rest) / len(rest), 3), "s")
print("rest fps  :", round(len(rest) / sum(rest), 1))