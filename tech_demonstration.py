#!/usr/bin/env python3
import math, threading
import numpy as np

import xgboost as xgb
import librosa
import sounddevice as sd
import serial, time
from melody_generator import MelodyGenerator
from midi_parser2 import parse_midi
from stuff import *
from cv2 import cv2
from math import sqrt, atan2, pi

import nxt
import classifier
from bbox_ops import *

waiting = False

def callback(indata, frames, time, status):
    if status:
        print(status)

    if any(indata):  
        mean = np.sqrt(np.mean(indata**2)) 
        print(mean)
        if (mean > 0.1) :
            global waiting 
            waiting = False
    else:
        print('no input')

def wait_sound():
    global waiting
    waiting = True

    with sd.InputStream(channels=1, callback=callback,
                        blocksize=int(samplerate * 0.05),
                        samplerate=samplerate):
        while waiting:
            pass
    print('heard')




bst = xgb.Booster()
bst.load_model('0001.model')
duration = 10
samplerate = sd.query_devices(None, 'input')['default_samplerate']

nechduino = serial.Serial('/dev/ttyACM0', 115200)
arduino = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(1) #give the connection a second to settle

model = classifier.Classifier(r'/home/tlab/Documents/models/frozen_inference_graph.pb')
cap = cv2.VideoCapture(2)
_, frame = cap.read()
boxes, scores, classes, num = model.get_classification(frame)

NXTs = {
    'zhmih': nxt.NXT('/dev/rfcomm0'),
    'nya': nxt.NXT('/dev/rfcomm2')
}

a = input()

nechduino.write([31])
nechduino.read()

def wait_a(a):
    global waiting
    waiting = True
    a.read()
    waiting = False
    print('!!!!')

waiting = True
t = threading.Thread(target=wait_a, args=(nechduino,))
t.start()

while waiting:
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
            if currNXT.firstpos[0] == -1:
                currNXT.firstpos = midOfRect(box)

            diff = currNXT.firstpos[1] - currNXT.pos[1],  -currNXT.firstpos[0] + currNXT.pos[0]
            angle = atan2(diff[0], diff[1]) / pi * 180
            if angle < 0:
                angle += 360
            angle += 180
            angle %= 360
            dist = sqrt(diff[0] ** 2 + diff[1] ** 2)

            cv2.arrowedLine(frame, currNXT.firstpos, currNXT.pos, (255, 255, 255))
            # if (cv2.getTickCount() - currNXT.timeSinceLastComm) / cv2.getTickFrequency() > COMMAND_FREQ and dist > MINDIST:
            if dist > MINDIST:
                currNXT.send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
                # print(int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10))
                currNXT.timeSinceLastComm = cv2.getTickCount()

            cv2.rectangle(frame, (int(box[1]*640), int(box[0]*480)), (int(box[3]*640), int(box[2]*480)), color_map[currClass])
            cv2.putText(frame, name_map[currClass], (int(box[1]*640), int(box[0]*480)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_map[currClass],2)
            cv2.putText(frame, str(scores[0][idx]), (int(box[1]*640+80), int(box[0]*480)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_map[currClass],2)

    for name, nxt in NXTs.items():
        if not nxt.ready and not nxt.stopped:
            nxt.stop()
            print(name + " stopped")

    # calc FPS and draw it
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

nechduino.write([32])
nechduino.read()

arduino.write([1])
arduino.read()

nechduino.write([32])
nechduino.read()

wait_sound()

arduino.write([1])

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()
sequence = process_recording(myrecording, samplerate, bst)
arduino.write([1])
arduino.read()

arduino.write([1])

nechduino.write([33])
nechduino.read()

time.sleep(3)

output = [names[x] for x in sequence[:4]]

s = ''
for x in output:
    s += x + " "
  # Not actually necessary if you just want to create an image.

blank_image = np.zeros((1080,1920,3), np.uint8)
blank_image[:] = (0, 0, 255)
cv2.putText(blank_image, s, (100, 500), 0, 10, (255, 255, 255), 30)
cv2.imshow('frame', blank_image)
cv2.waitKey(2000)

nechduino.write([34])
nechduino.read()

nechduino.write([32])
nechduino.read()

gen = MelodyGenerator()
melody = gen.generate(sequence[:4])
print(len(melody))

gen.write_midi(melody, 'midi/m.mid')

melody = parse_midi('midi/m.mid')

wait_sound()

for x in melody:
    arduino.write([x[0]])
    arduino.write([x[1]])
    arduino.write([x[2] >> 8])
    arduino.write([x[2] & 255])
    arduino.read()

arduino.read()

nechduino.write([32])
nechduino.read()

arduino.write([1])

nechduino.write([34])
nechduino.read()

melody = parse_midi('midi/ode2.mid')
wait_sound()

for x in melody:
    arduino.write([x[0]])
    arduino.write([x[1]])
    arduino.write([x[2] >> 8])
    arduino.write([x[2] & 255])
    arduino.read()

arduino.read()
