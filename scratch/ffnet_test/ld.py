### stock problem example for ffnet ###

# Data and description for this example is borrowed from:
# http://www.scientific-consultants.com/nnbd.html
#
#
# Training data consists of Black-Scholes option prices
# for volatility levels running from 20 percent to 200 percent,
# for time remaining running from 5 to 15 days, and for strike price
# running from 70 dollars to 130 dollars. The stock price was set to
# 100 dollars and the interest rate to 0 percent when generating
# the data.
#
# The data is "difficult" in that (for a neural network to
# practically emulate Black-Scholes) a very tight fit is required.
# The R-squared should be at least 0.999999 or better, and the largest
# absolute error must be less than 0.05 dollars (the price increment
# for most options) or, better yet, less than 0.01 dollars.
#
#
# So let's try.
# Attention: training might be a long process since we train a big network.

from ffnet import ffnet, mlgraph, readdata
from numpy import array
import numpy as np

# Generate standard layered network architecture and create network
conec = mlgraph((3, 22, 12, 1))
net = ffnet(conec)

# Read training data omitting first column and first line
print "READING DATA..."
# data = readdata('black-scholes.dat',
#                  usecols=(1, 2, 3, 4),
#                  skiprows=1)
data_ld = np.loadtxt('ld.csv', delimiter=';')
data_par = np.loadtxt('inputs_frame_30sim.txt')
data_ld_x = data_ld[np.arange(0, 60, 2)]
# data_ld_x /= np.max(data_ld_x)
data_ld_y = data_ld[np.arange(1, 61, 2)]
# data_ld_y /= np.max(data_ld_y)
# input = data[:, :3]  # first 3 columns
# target = data[:, -1]  # last column
input = np.vstack((data_ld_x.flatten(), data_par[0, :].repeat(51), data_par[1, :].repeat(51))).T
target = data_ld_y.flatten()


# print "FINDING STARTING WEIGHTS WITH GENETIC ALGORITHM..."
# net.train_genetic(input, target, individuals=20, generations=500)
print "TRAINING NETWORK..."
import sys; sys.stdout.flush()  # Just to ensure dislpaing the above messages here
net.train_tnc(input, target, maxfun=50000)  # , messages=1)

# Test network
print
print "TESTING NETWORK..."
output, regression = net.test(input, target, iprint=0)
Rsquared = regression[0][2]
maxerr = abs(array(output).reshape(len(output)) - array(target)).max()
print "R-squared:           %s  (should be >= 0.999999)" % str(Rsquared)
print "max. absolute error: %s  (should be <= 0.05)" % str(maxerr)
print
print "Is ffnet ready for a stock?"

#####################################
# Make plot if matplotlib is avialble
try:
    from pylab import *
    plot(data_ld_x.flatten(), target, 'b--')
    plot(data_ld_x.flatten(), output, 'k-')
    legend(('target', 'output'))
    xlabel('pattern'); ylabel('price')
    title('Outputs vs. target of trained network.')
    grid(True)
    show()
except ImportError, e:
    print "Cannot make plots. For plotting install matplotlib.\n%s" % e
