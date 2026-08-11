import cv2

cap = cv2.VideoCapture("clip.mp4")
print("opened:", cap.isOpened())

claimed = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
print("claimed frames:", claimed, " claimed fps:", fps)

n = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    n += 1

cap.release()
print("actually read:", n)
print("duration:", n / fps, "seconds")