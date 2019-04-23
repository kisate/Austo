import xgboost as xgb
import numpy as np
import pickle
import json
import librosa
import operator

duration = 5

with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

classes = {
    'A'  : 0,
    'Am' : 1,
    'A#' : 2,
    'Am#': 3,
    'B'  : 4,
    'Bm' : 5,
    'C'  : 6,
    'Cm' : 7,
    'C#' : 8,
    'Cm#': 9,
    'D'  : 10,
    'Dm' : 11,
    'D#' : 12,
    'Dm#': 13,
    'E'  : 14,
    'Em' : 15,
    'F'  : 16,
    'Fm' : 17,
    'F#' : 18,
    'Fm#': 19,
    'G'  : 20,
    'Gm' : 21,
    'G#' : 22,
    'Gm#': 23
    }

names = ['A', 'Am', 'A#', 'Am#', 'B', 'Bm', 'C', 'Cm', 'C#', 'Cm#', 'D', 'Dm', \
 'D#', 'Dm#', 'E', 'Em', 'F', 'Fm', 'F#', 'Fm#', 'G', 'Gm', 'G#', 'Gm#']


scales = {}

def init_scales():
    for i, name in enumerate(names):
        scale = [0]*24
        scale[i] = 10
        scale[(i+10) % 24] = 4
        scale[(i+14) % 24] = 5
        scales[name] = scale 



bst = xgb.Booster()
bst.load_model('0001.model')


waiting = True
print('waiting')

try:
    import sounddevice as sd

    samplerate = sd.query_devices(None, 'input')['default_samplerate']

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

    with sd.InputStream(channels=1, callback=callback,
                        blocksize=int(samplerate * 0.05),
                        samplerate=samplerate):
        while waiting:
            pass
            
except KeyboardInterrupt:
    print('Interrupted by user')
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))

print('recording {} seconds'.format(duration))

myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)

sd.wait()

print('done')

y = np.array([x[0] for x in myrecording])
print(y)

ind = 0
while (y[ind] < 0.1):
    ind += 1
y = y[ind:]
ind = len(y)
while (y[ind - 1] < 0.1):
    ind -= 1
y = y[:ind]

print(y)

chroma_orig = librosa.feature.chroma_cqt(y=y, sr=samplerate)

onset_env = librosa.onset.onset_strength(y, sr=samplerate)
tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=samplerate)

print(tempo)

l = len(chroma_orig[0])

features = []

for i in range(l//5):
    buf = []
    for j in range(i*5, min(l, (i+1)*5)):
        buf.extend([chroma_orig[x][j] for x in range(12)])
    features.append(buf)

dfeats = xgb.DMatrix(features)
y_pred = bst.predict(dfeats)

chords_in_recording = []

for x in y_pred:
        
    chord = x.argmax(axis=0)
        
    if (max(x) > 0.9) : 
        
        print("{} {}".format(max(x), names[chord]))
        chords_in_recording.append(chord)

    else : 
        
        print("{} {}?".format(max(x), names[chord]))
        chords_in_recording.append(-1)

scale = ('A', 0)
amount = 0
counts = {}

print(chords_in_recording)

for chord in chords_in_recording:
    if chord > - 1:
        if chord in counts.keys():
            counts[chord] += 1
        else :
            counts[chord] = 1
    amount += 1
print(counts)

for x in scales.keys():
    score = 0
    for chord in counts.keys():
        if counts[chord] > amount * 0.05:
            score += scales[x][chord]
    if score > scale[1]:
        scale = (x, score)
s = ''
for c in chords_in_recording:
    if (c > -1) : s += names[c] + ' '

print(scale)
print(s)

sequence = []
scores = {}

for chord in chords_in_recording:    
    if chord > -1 :
        if chord in scores.keys():
            scores[chord] += 1
        else :
            scores[chord] = 1
        if scores[chord] == 6:
            for key in scores.keys():
                if key != chord:
                    scores[key] = 0
            sequence.append(chord)
print(sequence)

from melody_generator import MelodyGenerator

gen = MelodyGenerator()

melody = gen.generate(sequence[:4])

print('playing')
print(melody)


melody.extend([12, 0])

import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
# arduino.write(b"Hello from Python!")

for x in melody:
    
    arduino.write(x)
    print(arduino.read())

