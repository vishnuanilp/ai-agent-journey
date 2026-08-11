import cv2, time
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

grab_total = 0.0
det_total = 0.0

for i in range(20):
    a = time.time()
    ok, frame = cap.read()
    b = time.time()
    if not ok:
        continue
    model(frame, verbose=False)
    c = time.time()
    grab_total += b - a
    det_total += c - b

cap.release()
print(f"grab avg   {grab_total/20:.3f}s")
print(f"detect avg {det_total/20:.3f}s")
print(f"combined   {20/(grab_total+det_total):.1f} fps")