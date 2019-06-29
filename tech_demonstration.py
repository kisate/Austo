#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""
import argparse
import math
import numpy as np
import shutil
import stuff
import xgboost as xgb
import librosa
import sounddevice as sd

chord = 'C'
bst = xgb.Booster()
bst.load_model('0001.model')
duration = 10

samplerate = sd.query_devices(None, 'input')['default_samplerate']

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()
sequence = stuff.process_recording(myrecording, samplerate, bst)
print(sequence)

output = [stuff.names[x] for x in sequence[:4]]

s = ''
for x in output:
    s += x + " "

import cv2  # Not actually necessary if you just want to create an image.
import numpy as np
blank_image = np.zeros((1080,1920,3), np.uint8)
blank_image[:] = (0, 0, 255)
cv2.cv2.putText(blank_image, s, (100, 500), 0, 10, (255, 255, 255), 30)
cv2.imshow('image', blank_image)
cv2.waitKey(1)

