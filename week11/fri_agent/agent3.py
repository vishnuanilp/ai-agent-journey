import cv2
from datetime import datetime, timedelta
from ultralytics import YOLO
from decide1 import decide

def run(path, fps, began, start, end, tag):
    model, cap = YOLO("../wed_video/yolov8n.pt"), cv2.VideoCapture(path)
    n, was, w, events = 0, False, None, []
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
            name = f"{tag}_{len(events)+1}.mp4"
            w = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (640, 480))
            events.append([name, ts, 0])
        if fired:
            w.write(frame)
            events[-1][2] += 1
        if was and not fired:
            w.release()
        was = fired
    if w and was:
        w.release()
    cap.release()
    print(f"{path}: {n} frames -> {len(events)} events")
    for e in events:
        print(f"   {e[0]}  {e[1]:%H:%M:%S}  {e[2]} frames")

run("../wed_video/clip.mp4", 11.0, datetime(2026, 8, 9, 19, 46), 19, 20, "clip")
run("empty.mp4", 24.5, datetime(2026, 8, 11, 17, 56), 19, 20, "empty")