from __future__ import print_function
import numpy as np
import scipy
import matplotlib.pyplot as plt

import librosa
import librosa.display

import pickle
import glob


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

data = [[], []]

for name in names:

    for fname in glob.glob('chords/{}/*'.format(name)):
        print("{} {}".format(fname, '/chords/' + name))
        y, sr = librosa.load(fname)
        chroma_orig = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        l = len(chroma_orig[0])

        d = 5
        step = 1

        for j in range(l//d):

            buf = []

            for g in range(j*d, min(l, (j+1)*d), step):
                buf.extend([chroma_orig[i][g] for i in range(12)])

            data[0].append (buf)
            data[1].append (classes[name])
        
        print (fname)
        print(len(data[0]))


with open('train/data/data.out', 'wb') as f:
    pickle.dump(data, f)