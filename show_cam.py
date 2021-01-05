import cv2

cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    cv2.imshow('f', frame)
    cv2.waitKey(1)