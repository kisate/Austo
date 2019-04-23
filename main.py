import xgboost as xgb
import sounddevice as sd
import numpy as np
import pickle
import json
import librosa
import operator

from stuff import *
duration = 5

mscales = [
    [0, 2, 4, 5, 7, 9, 11], #maj
    [0, 2, 3, 5, 7, 8, 10] #min
]

with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

samplerate = sd.query_devices(None, 'input')['default_samplerate']

bst = xgb.Booster()
bst.load_model('0001.model')


waiting = True
print('waiting')

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
                

    print('recording {} seconds'.format(duration))

wait_sound()

import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
arduino.write([1])

wait_sound()

arduino.write([1])
time.sleep(1)

wait_sound()

arduino.write([1])

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()
sequence = process_recording(myrecording, samplerate, bst)
print(sequence)


from melody_generator import MelodyGenerator

gen = MelodyGenerator()
melody = gen.generate(sequence[:4])

prefix = [sequence[0] // 4, 4, (sequence[0] // 4 + mscales[sequence[0] % 2][3]) % 12, 4, (sequence[0] // 4 + mscales[sequence[0] % 2][4]) % 12, 4, (sequence[0] // 4 + mscales[sequence[0] % 2][5]) % 12, 4]
melody.extend([12, 0])

prefix.extend(melody)


for x in prefix:
    
    arduino.write([x])
    print(arduino.read())
    

