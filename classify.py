import tensorflow as tf
import cv2
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

class Classifier(object):
    def __init__(self):
        PATH_TO_MODEL = r'/home/tlab/Documents/models/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')
        self.sess = tf.Session(graph=self.detection_graph)


    def get_classification(self, img):
        with self.detection_graph.as_default():
            img_expanded = np.expand_dims(img, axis=0)  
            (boxes, scores, classes, num) = self.sess.run(
                [self.d_boxes, self.d_scores, self.d_classes, self.num_d],
                feed_dict={self.image_tensor: img_expanded})
        return boxes, scores, classes, num

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

cap = cv2.VideoCapture(1)

NXTs = {
    'zhmih': NXT('/dev/rfcomm0'),
    'nya': NXT('/dev/rfcomm2')
}

model = Classifier()

a = input()

name_map = {
    1:'zhmih',
    2:'nya'
}

color_map = {
    1:(0,255,255),
    2:(0,0,255),
    3:(255,0,0)
}

while True:
    timer = cv2.getTickCount()
    ok, frame = cap.read()
    boxes, scores, classes, num = model.get_classification(frame)

    cnt = 0
    c = []
    goodBoxes = []

    for _, nxt in NXTs.items():
        nxt.ready = False

    for idx, box in enumerate(boxes[0]):
        if scores[0][idx]>0.9 and cnt < 2 and classes[0][idx] != 3 and (classes[0][idx] not in c):
            boxesOverlap = False
            for b in goodBoxes:
                if (area(intersection(b, box)) / area(b) > 0.6):
                    boxesOverlap = True
                    print('overlapped')
                    break
            if boxesOverlap:
                continue

            goodBoxes.append(box)
            c.append(classes[0][idx])
            cnt+=1

            currClass = int(classes[0][idx])
            currNXT = NXTs[name_map[currClass]]
            currNXT.ready = True

            currNXT.pos = midOfRect(box)
            # print(currNXT.pos)
            # print(currNXT.firstpos)
            if currNXT.firstpos[0] == -1:
                currNXT.firstpos = midOfRect(box)

            diff = currNXT.firstpos[1] - currNXT.pos[1],  -currNXT.firstpos[0] + currNXT.pos[0]
            angle = atan2(diff[0], diff[1]) / pi * 180
            if angle < 0:
                angle += 360
            angle += 180
            angle %= 360
            print(angle)
            dist = sqrt(diff[0] ** 2 + diff[1] ** 2)

            cv2.arrowedLine(frame, currNXT.firstpos, currNXT.pos, (255, 255, 255))
            # if (cv2.getTickCount() - currNXT.timeSinceLastComm) / cv2.getTickFrequency() > COMMAND_FREQ and dist > MINDIST:
            if dist > MINDIST:
                currNXT.send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
                print(int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10))
                currNXT.timeSinceLastComm = cv2.getTickCount()

            cv2.rectangle(frame, (int(box[1]*640), int(box[0]*480)), (int(box[3]*640), int(box[2]*480)), color_map[currClass])
            cv2.putText(frame, name_map[currClass], (int(box[1]*640), int(box[0]*480)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_map[currClass],2)

    for name, nxt in NXTs.items():
        if not nxt.ready:
            nxt.stop()
            print(name + " stopped")

    # calc FPS and draw it
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)