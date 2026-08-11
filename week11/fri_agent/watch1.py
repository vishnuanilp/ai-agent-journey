import cv2

cap = cv2.VideoCapture("../wed_video/clip.mp4")
n = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    n += 1
    print(f"frame {n}", end="\r")
cap.release()
print(f"\nfeed ended after {n} frames")