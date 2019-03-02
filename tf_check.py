import tensorflow as tf
import numpy as np
import pickle
import json

import librosa
import librosa.display
import matplotlib.pyplot as plt

import sounddevice as sd

sd.default.device = 7

with open('train/data/config.json') as f:
    config = json.load(f)

train_dir = config['train_dir']

names = ['A', 'Am', 'B', 'Bm', 'C', 'Cm', 'D', 'Dm', 'E', 'Em', 'F', 'Fm', 'G', 'Gm']

sess = tf.Session()

saver = tf.train.import_meta_graph(train_dir + 'model.ckpt.meta')
saver.restore(sess, tf.train.latest_checkpoint(train_dir))

graph = tf.get_default_graph()

keep_prob = graph.get_tensor_by_name('drop_prob:0')
X = graph.get_tensor_by_name('features:0')
a = graph.get_tensor_by_name(name='activationOutputLayer:0')

print('ready')

line = input()

while line != 'end':

    line = input()

    duration = 5
    fs = 44100

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    
    sd.wait()
    
    y = np.array([x[0] for x in myrecording])

    chroma_orig = librosa.feature.chroma_cqt(y=y, sr=fs)


    ts_features = [[chroma_orig[i][x] for i in range(12)] for x in range(len(chroma_orig))]

    print(ts_features[0])
    print(ts_features[1])

    y_pred = sess.run(tf.argmax(a, 1), feed_dict={X: ts_features,keep_prob:1.0})
    
    print(y_pred)
    


    line = input()



sess.close()