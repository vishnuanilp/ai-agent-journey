import cv2

cap = cv2.VideoCapture(0)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("size:", w, h)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("clip.mp4", fourcc, 11.0, (w, h))

for i in range(110):
    ok, frame = cap.read()
    if not ok:
        continue
    out.write(frame)

out.release()
cap.release()
print("wrote clip.mp4")