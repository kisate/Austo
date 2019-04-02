import xgboost as xgb
import numpy as np
import pickle
import json

import librosa
import librosa.display
import matplotlib.pyplot as plt

import sounddevice as sd


with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

names = ['A', 'Am', 'B', 'Bm', 'C', 'Cm', 'D', 'Dm', 'E', 'Em', 'F', 'Fm', 'G', 'Gm']

bst = xgb.Booster()
bst.load_model('0001.model')


print('ready')

line = input()

while line != 'end':

    line = input()

    duration = 10
    fs = 44100

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    
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

    chroma_orig = librosa.feature.chroma_cqt(y=y, sr=fs)

    onset_env = librosa.onset.onset_strength(y, sr=fs)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=fs)

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
    
    for x in y_pred:
        if (max(x) > 0.7) : print("{} {}".format(max(x), names[x.argmax(axis=0)]))
        else : print("{} {}?".format(max(x), names[x.argmax(axis=0)]))

    line = input()


