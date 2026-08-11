import cv2
from datetime import datetime
from ultralytics import YOLO
from decide1 import decide

def run(path, start, end):
    model = YOLO("../wed_video/yolov8n.pt")
    cap = cv2.VideoCapture(path)
    n = fired = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        n += 1
        r = model(frame, verbose=False)[0]
        people = sum(1 for b in r.boxes if int(b.cls[0]) == 0)
        if decide(people, datetime.now(), start, end):
            fired += 1
    cap.release()
    print(f"{path}: {n} frames, {fired} fired")

run("../wed_video/clip.mp4", 22, 6)
run("empty.mp4", 22, 6)