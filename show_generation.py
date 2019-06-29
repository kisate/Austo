import numpy as np
import sounddevice as sd
from stuff import *
import json
from midi_parser2 import parse_midi

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

gen.write_midi(melody, 'midi/m.mid')


melody = parse_midi('midi/m.mid')

print(melody)

import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
# arduino.write(b"Hello from Python!")

print(len(melody))

for x in melody:
    arduino.write([x[0]])
    arduino.write([x[1]])
    arduino.write([x[2] >> 8])
    arduino.write([x[2] & 255])
    arduino.read()

