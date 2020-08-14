import math
import numpy as np
import os

from . import utils

def sigmoid(x):
    """ computes sigmoid of x """
    return 1.0/(1.0 + np.exp(-x))

def mutate(genome):
    """ mutates a genome and returns the mutated one """
    # mutate some random indices by a certain amount

    # only mutate with a certain probability
    if np.random.random() < 0.5:
        return genome

    l = len(genome)
    indices = np.random.choice(l, int(l * utils.MUTATION_PROB), replace=False)
    li = len(indices)
    # mutate
    genome[indices] += np.random.random() - 0.5
    return genome

def cross_over(m1_vec, m2_vec):
    """ performs cross over between two genomes """
    # interchange a random amount of both vectors
    l = len(m1_vec)
    indices = np.random.choice(l, np.random.randint(0, int(l * utils.CROSS_OVER_PROB)), replace=False)

    temp = m1_vec[indices][:]
    m1_vec[indices] = m2_vec[indices][:]
    m2_vec[indices] = temp[:]

    return m1_vec, m2_vec

class Model:
    """ holds the brain of an agent """
    def __init__(self):
        # create weights
        self.W1 = 2.0 * np.random.random((4, 6)) - 1.0
        self.W2 = 2.0 * np.random.random((3, 5)) - 1.0
        self.W3 = 2.0 * np.random.random((2, 4)) - 1.0

    def get_weights(self):
        """ returns a vector with all weights """
        # returns a huge vector of all weights
        w1 = self.W1.flatten()
        w2 = self.W2.flatten()
        w3 = self.W3.flatten()
        ret = np.zeros(24 + 15 + 8,dtype=float)
        ret[:24] = w1
        ret[24:39] = w2
        ret[39:] = w3
        return ret

    def save_to_file(self, filename):
        np.savetxt(os.path.join(utils.MODELS_PATH, filename), self.get_weights())

    def load_from_file(self, filename):
        self.set_weights(np.loadtxt(os.path.join(utils.MODELS_PATH, filename)))

    def set_weights(self, w):
        """ set weights from a vector """
        self.W1 = w[:24].reshape((4,6))
        self.W2 = w[24:39].reshape((3,5))
        self.W3 = w[39:].reshape((2,4))

    def predict(self, inp):
        # add a bias term to inp
        x = np.ones((6,1),dtype=float)
        x[:5, 0] = inp
        # we have now (inp, 1) inside x

        # forward propagation:
        x1 = self.W1.dot(x)
        #x1 = np.maximum(0.0, x1) # relu
        #x1 = sigmoid(x1)
        x1_ = np.ones((5,1), dtype=float)
        x1_[:4, 0] = x1[:,0]

        x2 = self.W2.dot(x1_)
        #x2 = np.maximum(0.0, x2) # relu
        #x2 = sigmoid(x2)
        x2_ = np.ones((4,1), dtype=float)
        x2_[:3,0] = x2[:,0]

        x3 = self.W3.dot(x2_)
        x3 = sigmoid(x3)
        #x3 = np.tanh(x3)
        #x3 = np.maximum(0.0, x3)

        return x3