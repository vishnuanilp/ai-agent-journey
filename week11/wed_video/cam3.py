import cv2, time

cap = cv2.VideoCapture(0)
print("opened:", cap.isOpened())

t0 = time.time()
grabbed = 0

for i in range(30):
    ok, frame = cap.read()
    if not ok:
        print(f"frame {i}: FAILED")
        continue
    grabbed += 1

elapsed = time.time() - t0
cap.release()
print(f"asked 30, got {grabbed}, in {elapsed:.2f}s = {grabbed/elapsed:.1f} fps")