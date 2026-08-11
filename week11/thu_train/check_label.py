import cv2

img = cv2.imread("images/f050.jpg")
h, w = img.shape[:2]

cx, cy, bw, bh = 0.891, 0.656, 0.219, 0.688
x1 = int((cx - bw / 2) * w)
y1 = int((cy - bh / 2) * h)
x2 = int((cx + bw / 2) * w)
y2 = int((cy + bh / 2) * h)

cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imwrite("check.jpg", img)
print("box drawn at:", x1, y1, x2, y2)