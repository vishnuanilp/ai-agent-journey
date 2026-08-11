import cv2
from datetime import datetime, timedelta
from ultralytics import YOLO
from decide1 import decide
from notify1 import build, send

def run(path, fps, began, start, end, tag, site):
    model, cap = YOLO("../wed_video/yolov8n.pt"), cv2.VideoCapture(path)
    n, was, w, ev = 0, False, None, None
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        n += 1
        ts = began + timedelta(seconds=n / fps)
        r = model(frame, verbose=False)[0]
        people = sum(1 for b in r.boxes if int(b.cls[0]) == 0)
        fired = decide(people, ts, start, end)
        if fired and not was:
            count += 1
            ev = [f"{tag}_{count}.mp4", ts, 0, people]
            w = cv2.VideoWriter(ev[0], cv2.VideoWriter_fourcc(*"mp4v"), fps, (640, 480))
        if fired:
            w.write(frame)
            ev[2] += 1
        if was and not fired:
            w.release()
            send(build(site, ev[0], ev[1], ev[2], fps, ev[3]))
        was = fired
    if w and was:
        w.release()
        send(build(site, ev[0], ev[1], ev[2], fps, ev[3]))
    cap.release()
    print(f"{path}: {n} frames -> {count} alert(s)")

run("../wed_video/clip.mp4", 11.0, datetime(2026, 8, 9, 19, 46), 19, 20, "ev", "Anjali Restaurant - back door")
run("empty.mp4", 24.5, datetime(2026, 8, 11, 17, 56), 19, 20, "ev", "Anjali Restaurant - back door")