import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("opened:", cap.isOpened())

ok, frame = cap.read()
print("ok:", ok)
print("type:", type(frame))
print("shape:", frame.shape)

cv2.imwrite("frame0.jpg", frame)
cap.release()
print("saved frame0.jpg")