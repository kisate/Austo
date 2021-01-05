import numpy as npy
from cv2 import cv2

def nothing(x):
    pass
cap = cv2.VideoCapture(1)

low1 = npy.array([75, 120, 172])
high1 = npy.array([180, 255, 255])
low2 = npy.array([255, 255, 255])
high2 = npy.array([255, 255, 255])

cv2.namedWindow('trackbars')

cv2.createTrackbar('h1','trackbars',0,255,nothing)
cv2.createTrackbar('s1','trackbars',0,255,nothing)
cv2.createTrackbar('v1','trackbars',0,255,nothing)

cv2.createTrackbar('h2','trackbars',0,255,nothing)
cv2.createTrackbar('s2','trackbars',0,255,nothing)
cv2.createTrackbar('v2','trackbars',0,255,nothing)



cv2.createTrackbar('h12','trackbars',0,255,nothing)
cv2.createTrackbar('s12','trackbars',0,255,nothing)
cv2.createTrackbar('v12','trackbars',0,255,nothing)

cv2.createTrackbar('h22','trackbars',0,255,nothing)
cv2.createTrackbar('s22','trackbars',0,255,nothing)
cv2.createTrackbar('v22','trackbars',0,255,nothing)



cameraOffset1 = 85

while True:  
    ret, frame = cap.read()
    frame = frame[:, cameraOffset1:]

    # low1 = npy.array([cv2.getTrackbarPos('h1','trackbars'),cv2.getTrackbarPos('s1','trackbars'), cv2.getTrackbarPos('v1','trackbars')])
    # high1 = npy.array([cv2.getTrackbarPos('h2','trackbars'),cv2.getTrackbarPos('s2','trackbars'), cv2.getTrackbarPos('v2','trackbars')])
    # low2 = npy.array([cv2.getTrackbarPos('h12','trackbars'),cv2.getTrackbarPos('s12','trackbars'), cv2.getTrackbarPos('v12','trackbars')])
    # high2 = npy.array([cv2.getTrackbarPos('h22','trackbars'),cv2.getTrackbarPos('s22','trackbars'), cv2.getTrackbarPos('v22','trackbars')])


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low1, high1)
    mask += cv2.inRange(hsv, low2, high2)    
    #mask += cv2.inRange(hsv, low3, high3)

    cv2.bitwise_and(hsv, hsv, mask = mask)
    connectivity = 7
    output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)

    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    
    for i in range(num_labels):
        x, y, w, h, s = stats[i]
        if s > 10000 and s < 70000:                
            
            cv2.rectangle(frame,(x, y), (x+w, y+h) , (0,255,0), 10)

    cv2.imshow('image', frame)
    cv2.imshow('mask', mask)

    k = cv2.waitKey(1)

    if k == ord('q'):
        cap.release()
        cv2.destroyAllWindows()  
        exit()
    elif k == ord('a'):
        print(low1)
        print(high1)
