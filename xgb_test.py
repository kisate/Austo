
from __future__ import division

import numpy as np
import xgboost as xgb
import json
import pickle

from sklearn.preprocessing import LabelBinarizer
from random import shuffle

with open('train/data/config.json') as f:
    config = json.load(f)

n_classes = config['n_classes']

n_neurons_h = config['neurons']
learning_rate = config['learning_rate']
training_epochs = config['epochs']

path_to_model = config['path_to_model']
path_to_events = config['path_to_events']
path_to_data = config['path_to_data']
train_dir = config['train_dir']
batchsize = config['batchsize']

with open(path_to_data, 'rb') as f:
    data = pickle.load(f)

features = data[0]


n_features = len(features[0])

labels = data[1]

indexes = [i for i in range(len(features))]
shuffle(indexes)

features = [features[x] for x in indexes]
labels = [labels[x] for x in indexes]


features = np.array(features)
labels = np.array(labels)

dtrain = xgb.DMatrix(features[:int(len(features)*0.8)], label=labels[:int(len(labels)*0.8)])
dtest = xgb.DMatrix(features[int(len(features)*0.8):], label=labels[int(len(labels)*0.8):])

param = {}
# use softmax multi-class classification
param['objective'] = 'multi:softprob'
# scale weight of positive examples
param['eta'] = 0.5
param['max_depth'] = 10
param['silent'] = 1
param['nthread'] = 4
param['subsample'] = 0.5
param['predictor'] = 'gpu_predictor'

param['num_class'] = 14

evallist = [(dtest, 'eval'), (dtrain, 'train')]

num_round = 1000
bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=500)

pred = bst.predict(dtest)

# for i, x in enumerate(pred):
#     print(x[labels[int(len(labels)*0.9):][i]])
#     print(x)

bst.save_model('0001.model')

