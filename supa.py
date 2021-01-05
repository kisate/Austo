from cv2 import cv2
import numpy as np

import sys
from time import time, sleep
import numpy as np
from math import atan2, pi, sqrt
from random import randint

import serial

MINDIST = 20 # minimal deviation in pix for NXT to move
COMMAND_FREQ = 0.2 # 1 sec between commands to NXTs
SPEED_COEF = 0.4 # speed per pixel of dist

low1 = np.array([75, 120, 172])
high1 = np.array([180, 255, 255])

class NXT():
    def __init__(self, port, baud=9600):
        self.port = port
        self.stopped = False
        self.ser = serial.Serial(port, baud, write_timeout=0)
        self.ready = False
        self.timeSinceLastComm = cv2.getTickCount()
        self.pos = -1, -1
        self.firstpos = -1, -1
    
    def send(self, vals_):
        try:
            vals = vals_.copy()
            for idx, val in enumerate(vals):
                vals[idx] = hex(val)[2:].zfill(4)
            buf = b'\x0A\x00\x80\x09\x00\x06'
            for val in vals:
                buf += bytes.fromhex(val[2:]) + bytes.fromhex(val[:-2])
            self.ser.write(buf)
            self.timeSinceLastComm = cv2.getTickCount()
        except:
            self.send(vals_)
    
    def reconnect(self):
        print('b')
        self.ser = serial.Serial(self.port, write_timeout=0)
    
    def rotate(self):
        vals = [0, 0, 1]
        self.send(vals)

    def stop(self):
        self.stopped = True
        vals = [0, 0, 2]
        self.send(vals)

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[2], b[2])
    h = min(a[3], b[3])
    if w<0 or h<0: return (0, 0, 0, 0)
    return (x, y, w, h)

def area(a):
    return (a[2] - a[0]) * (a[3] - a[1])

def midOfRect(r):
    return ( int((r[3] + r[1]) * 640) // 2, int((r[2] + r[0]) * 480) // 2)


def mouse_callback(event,x,y,flags,param):
    global click_pos
    if event == cv2.EVENT_LBUTTONDBLCLK:
        click_pos = x,y

cap = cv2.VideoCapture(1)

NXTs = {
    'zhmih': NXT('/dev/rfcomm0'),
    'nya': NXT('/dev/rfcomm2')
}

a = input()


cameraOffset1 = 85
waiting = True

while waiting:  
    ret, frame = cap.read()
    frame = frame[:, cameraOffset1:]


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low1, high1)
    # mask += cv2.inRange(hsv, low2, high2)    
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
            waiting = False

    cv2.imshow('image', frame)
    cv2.imshow('mask', mask)

    k = cv2.waitKey(1)

    if k == ord('q'):
        cap.release()
        cv2.destroyAllWindows()  
        exit()

for i in range(60):
    # NXTs['zhmih'].send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
    NXTs['nya'].send([270, 50, int(COMMAND_FREQ * 10)])
    sleep(0.05)

for i in range(60):
    # NXTs['zhmih'].send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
    NXTs['zhmih'].send([270, 50, int(COMMAND_FREQ * 10)])
    sleep(0.05)