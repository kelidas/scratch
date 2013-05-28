# Back-Propagation Neural Networks
#
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Neil Schemenauer <nas@arctrix.com>

import math
import random
import string
import numpy as np

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b - a) * random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y ** 2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1  # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no

        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni - 1:
            raise ValueError, 'wrong number of inputs'

        # input activations
        for i in range(self.ni - 1):
            # self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            summ = 0.0
            for i in range(self.ni):
                summ = summ + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(summ)

        # output activations
        for k in range(self.no):
            summ = 0.0
            for j in range(self.nh):
                summ = summ + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(summ)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N * change + M * self.co[j][k]
                self.co[j][k] = change
                # print N*change, M*self.co[j][k]

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5 * (targets[k] - self.ao[k]) ** 2
        return error


    def test(self, ins):
        for p in ins:
            print p, '->', self.update(p)

    def weights(self):
        print 'Input weights:'
        for i in range(self.ni):
            print self.wi[i]
        print
        print 'Output weights:'
        for j in range(self.nh):
            print self.wo[j]

    def train(self, ins, tar, iterations=10000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in xrange(iterations):
            error = 0.0
            for inp, out in zip(ins, tar):
                inputs = inp
                targets = out
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 1000 == 0:
                print 'error %-14f' % error

def normalize_0to1(arr):
    min_vals = arr.min(axis=0)
    data_start = arr - min_vals
    max_vals = data_start.max(axis=0)
    data_norm = data_start / max_vals
    return data_norm

def normalize_min1to1(arr):
    min_vals = arr.min(axis=0)
    data_start = arr - min_vals
    max_vals = data_start.max(axis=0)
    data_norm = data_start / max_vals * 2 - 1
    return data_norm


def demo():
    # Teach network XOR function
    data = np.loadtxt('data_MC_32sim.txt', delimiter='\t', skiprows=1,
                      usecols=(0, 1, 3, 4, 8))

    inputs = data[:, :-1]
    target = data[:, -1]

    ins = normalize_min1to1(inputs)
    tar = normalize_min1to1(target)
    ins = ins.tolist()
    tar = tar[:, None].tolist()
    print  ins
    print tar




#     pat = [
#         [[0, 0], [0]],
#         [[0, 1], [1]],
#         [[1, 0], [1]],
#         [[1, 1], [0]]
#     ]

    # create a network with two input, two hidden, and one output nodes
    n = NN(4, 10, 1)
    # train it with some patterns
    n.train(ins, tar)
    # test it
    n.test(ins)
    n.weights()



if __name__ == '__main__':
    demo()

