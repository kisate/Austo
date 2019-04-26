import librosa
import numpy as np
import xgboost as xgb

note_codes = {
    'A' : 0,
    'A#': 1,
    'B' : 2,
    'C' : 3,
    'C#': 4,
    'D' : 5,
    'D#': 6,
    'E' : 7,
    'F' : 8,
    'F#': 9,
    'G' : 10,
    'G#': 11
    } 
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
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


name_map = {
    1:'zhmih',
    2:'zhizha',
    3:'nya'
}

color_map = {
    1:(0,255,255),
    2:(0,0,255),
    3:(255,0,0)
}

MINDIST = 50 # minimal deviation in pix for NXT to move
COMMAND_FREQ = 0.2 # 1 sec between commands to NXTs
SPEED_COEF = 0.4 # speed per pixel of dist

def process_recording(recording, samplerate, booster):
    y = np.array([x[0] for x in recording])
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
    y_pred = booster.predict(dfeats)

    chords_in_recording = []

    for x in y_pred:
            
        chord = x.argmax(axis=0)
            
        if (max(x) > 0.9) : 
            
            print("{} {}".format(max(x), names[chord]))
            chords_in_recording.append(chord)

        else : 
            
            print("{} {}?".format(max(x), names[chord]))
            chords_in_recording.append(-1)

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

    s = ''
    for c in chords_in_recording:
        if (c > -1) : s += names[c] + ' '

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
    return sequence
