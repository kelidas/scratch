#!/usr/bin/env python
# -*- coding: cp1250 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pylab import savefig

mu, sigma = 1000, 400
# x = mu + sigma*np.random.randn(10000)

x = np.loadtxt( 'CSN-Weibull-200ksim.txt' )

# the histogram of the data
n, bins, patches = plt.hist( x, 50, normed=1, facecolor='green', alpha=1 )

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma )
l = plt.plot( bins, y, 'r--', linewidth=1 )

plt.xlabel( 'g(X) = R - E' )
plt.ylabel( 'Probability' )
plt.title( r'$\mathrm{Histogram\ of\ } g(X)$' )
plt.axis( [-500, 4000, 0, 0.0012] )
plt.grid( True )





z = np.loadtxt( 'EC-Weibull-200ksim.txt' )

# the histogram of the data
n, bins, patches = plt.hist( z, 50, normed=1, facecolor='orange', alpha=0.5 )

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma )
l = plt.plot( bins, y, 'r--', linewidth=1 )

fname = open( 'image.eps', 'w' )
savefig( fname, format='eps',
          transparent=True )
fname.close()

plt.show()
