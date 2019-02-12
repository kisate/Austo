import librosa
import numpy as np
import math
from scipy.special import expit

def sigmoid(x):
    return  1 / (1 + math.exp(-x))  


class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x
        self.y          = y
        self.weights1   = np.random.rand(self.input.shape[0],self.y.shape[0]) 
        self.weights2   = np.random.rand(self.y.shape[0],1)                 
        self.output     = np.zeros(y.shape)
        

    def feedforward(self):
        self.layer1 = expit(np.dot(self.input, self.weights1))
        self.output = expit(np.dot(self.layer1, self.weights2))

nn = NeuralNetwork(np.array([1,2,3]), np.array([4]))