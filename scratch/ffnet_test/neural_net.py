
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List, Interface, implements, \
    Either, Enum, String, PythonValue, Any, Dict
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, HGroup, OKButton, CodeEditor, UItem, \
        VGroup, HSplit, EnumEditor, Handler, SetEditor, EnumEditor, InstanceEditor, \
        HTMLEditor, ShellEditor, CheckListEditor, VFlow, Label
import random
import numpy as np

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b - a) * random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
#     m = []
#     for i in range(I):
#         m.append([fill] * J)
#     print m
#     return m
    print np.zeros((I, J)) + fill
    return np.zeros((I, J)) + fill

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return np.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y ** 2

class NN(HasTraits):

    ins = Array
    out = Array

    ni = Int
    nh = Int
    no = Int

    # N: learning rate
    N = Float(0.5)
    # M: momentum factor
    M = Float(0.1)
    iterations = Int(10000)

    ai = Array
    def _ai_default(self):
        return np.ones((self.ins.shape[0], self.ni))

    ah = Array
    def _ah_default(self):
        return np.ones((self.ins.shape[0], self.nh))

    ao = Array
    def _ao_default(self):
        return np.ones_like(self.outs)

    wi = Array
    wo = Array

    ci = Array
    co = Array


    def __initd__(self):
        # activations for nodes
        self.ai = np.ones_like(self.ins)
        self.ah = np.ones(self.nh)
        self.ao = np.ones_like(self.outs)  # [1.0] * self.no

        # create weights
        self.wi = np.random.rand(self.ni, self.nh) * 0.4 - 0.2  # makeMatrix(self.ni, self.nh)
        self.wo = np.random.rand(self.nh, self.no) * 4 - 2  # makeMatrix(self.nh, self.no)
        # set them to random vaules
#         for i in range(self.ni):
#             for j in range(self.nh):
#                 self.wi[i][j] = rand(-0.2, 0.2)
#         for j in range(self.nh):
#             for k in range(self.no):
#                 self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self):
        if self.ins.shape[1] != self.ni:
            raise ValueError, 'wrong number of inputs'

        # input activations
        self.ai = self.ins

        # hidden activations
        for j in range(self.nh):
            summ = np.sum(self.ai * self.wi[j])
            self.ah[j] = sigmoid(summ)

        # output activations
        for k in range(self.no):
            summ = np.sum(self.ah * self.wo[k])
            self.ao[k] = sigmoid(summ)

        return self.ao[:]


    def backPropagate(self):
        if self.outs.shape[1] != self.no:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        error = self.outs - self.ao
        output_deltas = dsigmoid(self.ao) * error

        # calculate error terms for hidden
        hidden_deltas = np.zeros(self.nh)
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + self.N * change + self.M * self.co[j][k]
                self.co[j][k] = change
                # print N*change, M*self.co[j][k]

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + self.N * change + self.M * self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(self.outs)):
            error = error + 0.5 * (self.outs[k] - self.ao[k]) ** 2
        return error


    def test(self, ins, outs):
#         for p in patterns:
#             print p[0], '->', self.update(p[0])
        print ins, '->', self.update(ins)

    def weights(self):
#         print 'Input weights:'
#         for i in range(self.ni):
#             print self.wi[i]
#         print
#         print 'Output weights:'
#         for j in range(self.nh):
#             print self.wo[j]
        print 'Input weights:'
        print self.wi
        print
        print 'Output weights:'
        print self.wo

    def train(self):
        for i in xrange(self.iterations):
            error = 0.0
            error = error + self.backPropagate()
            if i % 100 == 0:
                print 'error %-14f' % error


def demo():

    ins = np.array([[0.33333, 1], [-1, -1], [1, 1]])
    outs = np.array([[-0.333333], [-1], [1]])

    # create a network with two input, two hidden, and one output nodes
    n = NN(ins=ins, outs=outs, ni=2, nh=2, no=1)
    # train it with some patterns
    import time
    start = time.time()
    n.train()
    print time.time() - start
    # test it
    n.test()



if __name__ == '__main__':
    demo()

