import cv2, os

src = r"D:\vocview\ai-agent-journey\week11\wed_video\clip.mp4"
out = "images"
os.makedirs(out, exist_ok=True)

cap = cv2.VideoCapture(src)
n = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    cv2.imwrite(os.path.join(out, f"f{n:03d}.jpg"), frame)
    n += 1
cap.release()
print("frames written:", n)