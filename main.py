import xgboost as xgb
import numpy as np
import pickle
import json
import librosa
import operator

duration = 10

with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

names = ['A', 'Am', 'B', 'Bm', 'C', 'Cm', 'D', 'Dm', 'E', 'Em', 'F', 'Fm', 'G', 'Gm']

classes = {
    'A' : 0, 
    'Am': 1,
    'B' : 2,
    'Bm': 3, 
    'C' : 4, 
    'Cm': 5, 
    'D' : 6, 
    'Dm': 7, 
    'E' : 8, 
    'Em': 9, 
    'F' : 10,
    'Fm': 11, 
    'G' : 12, 
    'Gm': 13
}

scales = {
    'A' : [10, 0, 0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 0, 0],
    'Am': [0, 10, 0, 0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 0],
    'B' : [0, 0, 10, 0, 0, 0, 0, 0, 4, 0, 5, 0, 0, 0],
    'Bm': [0, 0, 0, 10, 0, 0, 0, 0, 0, 4, 0, 5, 0, 0],
    'C' : [0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 4, 0, 5, 0],
    'Cm': [0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 4, 0, 5],
    'D' : [5, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 4, 0],
    'Dm': [0, 5, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 4],
    'E' : [4, 0, 5, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0],
    'Em': [0, 4, 0, 5, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
    # 'F' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
    # 'Fm': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], 
    'G' : [0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 0, 0, 10, 0],
    'Gm': [0, 0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 0, 0, 10]
}
 



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

            # if (mean > 0.1):
            #     y = np.array([x[0] for x in indata])
            #     ind = 0
            #     while (y[ind] < 0.1):
            #         ind += 1
            #     y = y[ind:]
            #     ind = len(y)
            #     while (y[ind - 1] < 0.1):
            #         ind -= 1
            #     y = y[:ind]

            #     print(y)

            #     chroma_orig = librosa.feature.chroma_cqt(y=y, sr=samplerate)

            #     onset_env = librosa.onset.onset_strength(y, sr=samplerate)
            #     tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=samplerate)

            #     print(tempo)

            #     l = len(chroma_orig[0])

            #     features = []

            #     for i in range(l//5):
            #         buf = []
            #         for j in range(i*5, min(l, (i+1)*5)):
            #             buf.extend([chroma_orig[x][j] for x in range(12)])
            #         features.append(buf)

            #     dfeats = xgb.DMatrix(features)
            #     y_pred = bst.predict(dfeats)
                
            #     for x in y_pred:
            #         if (max(x) > 0.7) : print("{} {}".format(max(x), names[x.argmax(axis=0)]))
            #         else : print("{} {}?".format(max(x), names[x.argmax(axis=0)]))

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


    # for chord in scores.keys():
    #     if scores[chord] == 3:
    #         chords_in_recording[i] = chord
    #         chords_in_recording[i + 1] = chord
    #         chords_in_recording[i + 2] = chord
    #         chords_in_recording[i + 3] = chord

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