from __future__ import print_function
import numpy as np
import scipy
import matplotlib.pyplot as plt

import librosa
import librosa.display


#######################################################################
# We'll use a track that has harmonic, melodic, and percussive elements
y, sr = librosa.load('audio/videoplayback.mp4')


#######################################
# First, let's plot the original chroma
chroma_orig = librosa.feature.chroma_cqt(y=y, sr=sr)

# For display purposes, let's zoom in on a 15-second chunk from the middle of the song

print(len(chroma_orig))
