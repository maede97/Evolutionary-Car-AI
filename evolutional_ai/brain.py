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

        self.layers = [int(x) for x in utils.HIDDEN_LAYERS.split(",")]

        # create weights
        self.weights = []
        if len(self.layers) == 0:
            # only input to output
            self.weights.append(2.0 * np.random.random((6, 2)) - 1.0)
        else:
            inp_size = 5
            for i in range(len(self.layers)):
                self.weights.append(2.0 * np.random.random((self.layers[i], inp_size + 1)) - 1.0)
                inp_size = self.layers[i]
            # append last
            self.weights.append(2.0 * np.random.random((2, inp_size + 1)) -1.0)

    def get_weights(self):
        """ returns a vector with all weights """
        # returns a huge vector of all weights

        # return self.weights, but flattened
        data = []
        for w in self.weights:
            wf = w.flatten()
            for x in wf:
                data.append(x)

        return np.array(data)

    def save_to_file(self, filename):
        # TODO add layer size
        np.savetxt(os.path.join(utils.MODELS_PATH, filename), self.get_weights())

    def load_from_file(self, filename):
        # TODO add layer size
        self.set_weights(np.loadtxt(os.path.join(utils.MODELS_PATH, filename)))

    def set_weights(self, w):
        """ set weights from a vector """
        i_w = 0
        x = 0
        y = 0
        for i in range(len(w)):
            self.weights[i_w][x, y] = w[i]
            y += 1
            if y == len(self.weights[i_w][0]):
                y = 0
                x += 1
                if x == len(self.weights[i_w]): # Error here
                    i_w += 1
                    x = 0
                

    def predict(self, inp):
        # add a bias term to inp
        x = np.ones((6,1),dtype=float)
        x[:5, 0] = inp
        # we have now (inp, 1) inside x

        # forward propagation:
        for layer in self.weights:
            x = layer.dot(x)
            x_ = np.ones((len(x)+1, 1), dtype=float)
            x_[:-1, 0] = x[:, 0]
            x = x_
        
        return sigmoid(x)