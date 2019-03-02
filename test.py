import librosa
import numpy as np
from math import exp, log
from scipy.special import expit
import pickle
import os

class NeuralNetwork:
    def __init__(self, size_in, size_out):
        self.size_in = size_in
        self.size_out = size_out
        self.weights1   = np.random.rand(size_in, 50) 
        self.weights2   = np.random.rand(50, size_out)
    
    def load(self, path):

        with open(path, 'rb') as fp:
            data = pickle.load(fp)

        self.size_in = data['size_in']
        self.size_out = data['size_out']
        self.weights1   = data['weights1'] 
        self.weights2   = data['weights2']

    def dump(self, path):
        
        data = {
            'size_in' : self.size_in,
            'size_out' : self.size_out,
            'weights1' : self.weights1,
            'weights2' : self.weights2
        }

        with open(path, 'wb') as fp:
            pickle.dump(data, fp)

    def feedforward(self):
        self.layer1 = expit(np.dot(input, self.weights1))
        return expit(np.dot(self.layer1, self.weights2))

    def backprop(self):
        d_weights2 = np.dot()




def softmax(vector):
    
    s = np.sum(np.apply_along_axis(exp, 0, vector))
    return np.apply_along_axis(lambda x : exp(x)/s, vector)

def count(model, batch, correct):
    
    _result = [model.feedforward(x) for x in batch]
    result = [softmax(x) for x in _result]

    #only for len 1 batch
    
    return -log(result[0][correct])




def train(path_to_data, path_to_model):
    with open(path_to_data, 'rb') as fp:
        dataset = pickle.load(fp)
    
    nn = NeuralNetwork(12, 14)

    if (os.path.isfile(path_to_model)) :
        with open(path_to_model, 'rb') as fp:
            model = pickle.load(fp)
            nn.load(model)
    
    with open(path_to_data, 'rb') as fp:
        indata = pickle.load(fp)
    
    for x in indata:
        
        y = count(nn, x[1], x[0])
        

    #[[0, [x12]], [1, [x12]], [2, [x12]], [1, [[], [], []]]
    #
    #
    #

nn = NeuralNetwork(np.array([1,2,3]), np.array([4]))