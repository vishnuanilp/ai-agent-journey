import cv2, time

cap = cv2.VideoCapture(0)
w = cv2.VideoWriter("empty.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 11.0, (640, 480))
print("recording 10s — leave the room NOW")
time.sleep(5)
start = time.time()
while time.time() - start < 10:
    ok, frame = cap.read()
    if ok:
        w.write(frame)
w.release()
cap.release()
print("saved empty.mp4")