import cv2
from datetime import datetime, timedelta
from ultralytics import YOLO
from decide1 import decide

def run(path, fps, began, start, end):
    model = YOLO("../wed_video/yolov8n.pt")
    cap = cv2.VideoCapture(path)
    n = fired = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        n += 1
        ts = began + timedelta(seconds=n / fps)
        r = model(frame, verbose=False)[0]
        people = sum(1 for b in r.boxes if int(b.cls[0]) == 0)
        if decide(people, ts, start, end):
            fired += 1
    cap.release()
    print(f"{path}: {n} frames, {fired} fired, last ts {ts:%H:%M:%S}")

run("../wed_video/clip.mp4", 11.0, datetime(2026, 8, 9, 19, 46), 22, 6)
run("empty.mp4", 24.5, datetime(2026, 8, 11, 17, 56), 22, 6)