
import ffnet
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

conec = ffnet.imlgraph((4, 4, 1), biases=True)
net = ffnet.ffnet(conec)

nx.draw_graphviz(net.graph, prog='dot')
plt.show()

data = np.loadtxt('data_MC_32sim.txt', delimiter='\t', usecols=(0, 1, 3, 4, 8),
                  skiprows=1)

input = data[:, :-1]
target = data[:, -1]

# print "FINDING STARTING WEIGHTS WITH GENETIC ALGORITHM..."
# net.train_genetic(input, target, individuals=20, generations=500)
print "TRAINING NETWORK..."
import sys; sys.stdout.flush()  # Just to ensure dislpaying the above messages here
# net.train_tnc(input, target, maxfun=5000, nproc=1, messages=1)
net.train_momentum(input, target, eta=0.2, momentum=0.8, maxiter=10000, disp=1)
# net.train_rprop(input, target)
# net.train_bfgs(input, target)
# net.train_genetic(input, target, individuals=20, generations=500)

# Test network
print
print "TESTING NETWORK..."
output, regression = net.test(input, target, iprint=1)
Rsquared = regression[0][2]
maxerr = abs(output.reshape(len(output)) - target).max()
print "R-squared:           %s  (should be >= 0.999999)" % str(Rsquared)
print "max. absolute error: %s  (should be <= 0.05)" % str(maxerr)
print
print "Is ffnet ready for a stock?"

#####################################
# Make plot if matplotlib is avialble
try:
    from pylab import *
    plot(target, 'b--')
    plot(output, 'k-')
    legend(('target', 'output'))
    xlabel('pattern'); ylabel('price')
    title('Outputs vs. target of trained network.')
    grid(True)
    show()
except ImportError, e:
    print "Cannot make plots. For plotting install matplotlib.\n%s" % e

# Plot results for first output
target = target[:, None]
plt.plot(target.T[0], output.T[0], 'o',
                        label='targets vs. outputs')
slope = regression[0][0]; intercept = regression[0][1]
x = linspace(0, 1)
y = slope * x + intercept
plt.plot(x, y, linewidth=2, label='regression line')
plt.legend()
plt.show()

print 'weights', net.weights
print 'conec', net.conec

for i in range(10):
    print net.weights[net.conec[:, 0] == i]
