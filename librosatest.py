from __future__ import print_function
import numpy as np
import scipy
import matplotlib.pyplot as plt

import librosa
import librosa.display

import pickle
import glob


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