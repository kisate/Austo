import xgboost as xgb
import numpy as np
import pickle
import json
import librosa
import sounddevice as sd
from cv2 import cv2
from math import atan2, pi, sqrt
import threading

import nxt
import classifier
from bbox_ops import *
from midi_parser2 import parse_midi
from stuff import *

duration = 10
sound_border = 0.1

mscales = [
    [0, 2, 4, 5, 7, 9, 11], #maj
    [0, 2, 3, 5, 7, 8, 10] #min
]

with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

samplerate = sd.query_devices(None, 'input')['default_samplerate']


import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(1) #give the connection a second to settle


# nechduino = serial.Serial('/dev/ttyACM0', 115200)
# time.sleep(1) #give the connection a second to settle


bst = xgb.Booster()
bst.load_model('0001.model')

# model = classifier.Classifier(r'/home/tlab/Documents/models/frozen_inference_graph.pb')

# cap = cv2.VideoCapture(1)

# _, frame = cap.read()
# boxes, scores, classes, num = model.get_classification(frame)

NXTs = {
    # 'zhmih': nxt.NXT('/dev/rfcomm0'),
    # 'nya': nxt.NXT('/dev/rfcomm2')
}

a = input()

waiting = True
print('waiting')

def callback(indata, frames, time, status):
    if status:
        print(status)
    if any(indata):
        
        mean = np.sqrt(np.mean(indata**2)) 
        print(mean)

        if (mean > sound_border) :
            global waiting 
            waiting = False

    else:
        print('no input')

def wait_sound(a=0.1):

    global waiting, sound_border
    waiting = True
    sound_border = a

    with sd.InputStream(channels=1, callback=callback,
                        blocksize=int(samplerate * 0.05),
                        samplerate=samplerate):
        while waiting:
            pass
                

    print('waiting for sound')

wait_sound()

arduino.write([1])
arduino.read()

# wait_sound()

time.sleep(1)

arduino.write([1])
arduino.read()

# wait_sound()

# arduino.write([1])
# arduino.read()

wait_sound()

arduino.write([1])
arduino.read()

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()
sequence = process_recording(myrecording, samplerate, bst)
print(sequence)


from melody_generator import MelodyGenerator

gen = MelodyGenerator()
melody = gen.generate(sequence[:4], 8)

melody.extend([20, 0])


for i in range(len(melody) // 2):
    
    arduino.write([melody[i*2], melody[i*2 + 1]])
    arduino.read()

time.sleep(0.5)

wait_sound()
arduino.write([1])
# waitingRotating = True

# def rotate():
#     global waitingRotating
#     while waitingRotating:
#         for _, nxt in NXTs.items():
#             nxt.rotate()
#         time.sleep(2.85)
#     print('a')
        
# t = threading.Thread(target=rotate)
# t.start()
arduino.read()

# waitingRotating = False

# for i in range(5):
#     timer = cv2.getTickCount()
#     ok, frame = cap.read()
#     print('1')
#     boxes, scores, classes, num = model.get_classification(frame)
#     print('2')

# nechduino.write([1])

def wait_a(a):
    global waiting
    waiting = True
    a.read()
    waiting = False
    print('!!!!')

# waiting = True
# t = threading.Thread(target=wait_a, args=(nechduino,))
# t.start()

# while waiting:
#     time.sleep(0.01)
    # timer = cv2.getTickCount()
    # ok, frame = cap.read()
    # boxes, scores, classes, num = model.get_classification(frame)
    # cnt = 0
    # c = []
    # goodBoxes = []

    # for _, nxt in NXTs.items():
    #     nxt.ready = False

    # for idx, box in enumerate(boxes[0]):
    #     if scores[0][idx]>0.9 and cnt < 2 and classes[0][idx] != 3 and (classes[0][idx] not in c):
    #         boxesOverlap = False
    #         for b in goodBoxes:
    #             if (area(intersection(b, box)) / area(b) > 0.6):
    #                 boxesOverlap = True
    #                 print('overlapped')
    #                 break
    #         if boxesOverlap:
    #             continue

    #         goodBoxes.append(box)
    #         c.append(classes[0][idx])
    #         cnt+=1

    #         currClass = int(classes[0][idx])
    #         currNXT = NXTs[name_map[currClass]]
    #         currNXT.ready = True

    #         currNXT.pos = midOfRect(box)
    #         if currNXT.firstpos[0] == -1:
    #             currNXT.firstpos = midOfRect(box)

    #         diff = currNXT.firstpos[1] - currNXT.pos[1],  -currNXT.firstpos[0] + currNXT.pos[0]
    #         angle = atan2(diff[0], diff[1]) / pi * 180
    #         if angle < 0:
    #             angle += 360
    #         angle += 180
    #         angle %= 360
    #         dist = sqrt(diff[0] ** 2 + diff[1] ** 2)

    #         cv2.arrowedLine(frame, currNXT.firstpos, currNXT.pos, (255, 255, 255))
    #         # if (cv2.getTickCount() - currNXT.timeSinceLastComm) / cv2.getTickFrequency() > COMMAND_FREQ and dist > MINDIST:
    #         if dist > MINDIST:
    #             currNXT.send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
    #             # print(int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10))
    #             currNXT.timeSinceLastComm = cv2.getTickCount()

    #         cv2.rectangle(frame, (int(box[1]*640), int(box[0]*480)), (int(box[3]*640), int(box[2]*480)), color_map[currClass])
    #         cv2.putText(frame, name_map[currClass], (int(box[1]*640), int(box[0]*480)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_map[currClass],2)
    #         cv2.putText(frame, str(scores[0][idx]), (int(box[1]*640+80), int(box[0]*480)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_map[currClass],2)

    # for name, nxt in NXTs.items():
    #     if not nxt.ready and not nxt.stopped:
    #         nxt.stop()
    #         print(name + " stopped")

    # # calc FPS and draw it
    # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    # cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    # cv2.imshow('frame', frame)
    # cv2.waitKey(1)
    # pass


# nechduino.read()

time.sleep(0.2)

wait_sound()

melody = parse_midi('midi/pirate2.mid')

for x in melody:
    arduino.write([x[0]])
    arduino.write([x[1]])
    arduino.write([x[2] >> 8])
    arduino.write([x[2] & 255])
    arduino.read()

wait_sound()
# nechduino.write([70])
arduino.write([1])
arduino.read()

# nechduino.write([7])
# nechduino.read()


