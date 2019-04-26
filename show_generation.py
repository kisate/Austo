import numpy as np
import sounddevice as sd
from stuff import *

waiting = True
duration = 10
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
                

    print('waiting for sound')

with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(1) #give the connection a second to settle

bst = xgb.Booster()
bst.load_model('0001.model')

samplerate = sd.query_devices(None, 'input')['default_samplerate']

wait_sound()

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
sd.wait()
sequence = process_recording(myrecording, samplerate, bst)
print(sequence)


from melody_generator import MelodyGenerator

gen = MelodyGenerator()
melody = gen.generate(sequence[:4])

melody.extend([20, 0])



for i in range(len(melody) // 2):
    
    arduino.write([melody[i*2], melody[i*2 + 1]])
    print(arduino.read())

