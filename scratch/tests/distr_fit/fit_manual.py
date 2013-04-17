'''
Created on Dec 5, 2010

@author: kelidas
'''

from numpy import loadtxt, isnan, linspace, sign
import matplotlib.pyplot as plt
from scipy.stats import beta, expon, betaprime, f, wald

data1 = loadtxt( 'slack.txt' ).flatten()
data1 = data1[data1 >= 0]
data2 = loadtxt( 'cf.txt' ).flatten()
data2 = data2[data2 >= 0]
data3 = loadtxt( 'cfl_cuts.txt' ).flatten()
data3 = data3[data3 >= 0]

class puniform():
    '''
        piecewise uniform distribution
    '''
    def pdf( self, x, a, b, m ):
        return m * Heaviside( a - x ) + ( 1 - m * a ) / ( b - a ) * Heaviside( x - a ) * Heaviside( b - x )
    def cdf( self, x, a, b, m ):
        return m * x * Heaviside( a - x ) + ( m * a + ( 1 - m * a ) / ( b - a ) * ( x - a ) ) * Heaviside( x - a ) * Heaviside( b - x )
    
rv1 = beta( .15, 5, 0, 0.06 )
x1 = linspace( 0, 0.2, 1000 )
rv2 = beta( .9, 1.5, 0, 100 )
x2 = linspace( 0, 100, 1000 )
rv3 = beta( .05, 1.2, 0, 6000 )
x3 = linspace( 0, 6000, 1000 )
rv4 = puniform()

#plt.figure( 1 )
#plt.hist( data1, bins=100, normed=1 )
#plt.plot( x1, rv1.pdf( x1 ) )
#plt.ylim( 0, 200 )
#
#plt.figure( 2 )
#plt.hist( data2, bins=20, normed=1 )
#plt.plot( x2, rv2.pdf( x2 ) )
#plt.ylim( 0, .03 )
#
#plt.figure( 3 )
#plt.hist( data3, bins=20, normed=1 )
#plt.plot( x3, rv3.pdf( x3 ) )
#plt.ylim( 0, 0.004 )

def Heaviside( x ):
    return ( sign( x ) + 1.0 ) / 2.0

def pdf( x, a, b, d, n ):
    return 2 * ( -d + n * a - n * x + x ) / ( -d + a ) / ( n * b - a - n * a + d ) * Heaviside( x - a ) * Heaviside( d - x ) + 2 * n * ( b - x ) / ( b - d ) / ( n * b - a - n * a + d ) * Heaviside( x - d ) * Heaviside( b - x )

def cdf( x, a, b, d, n ):
    return - ( -Heaviside( -d + x ) * x ** 2 * b + Heaviside( -d + x ) * x ** 2 * d + 2 * d ** 2 * Heaviside( x - a ) * x - 2 * d ** 2 * Heaviside( x - a ) * a - 2 * d ** 2 * Heaviside( -d + x ) * x - Heaviside( -d + x ) * d ** 2 * b + Heaviside( x - a ) * x ** 2 * b - Heaviside( x - a ) * x ** 2 * d - Heaviside( x - a ) * a ** 2 * b + Heaviside( x - a ) * a ** 2 * d + 2 * d * Heaviside( x - a ) * a * b - 2 * n * a * Heaviside( x - a ) * x * d + 2 * n * a * Heaviside( -d + x ) * x * d - 2 * n * b * Heaviside( -d + x ) * x * d + 2 * n * b * Heaviside( x - b ) * x * d - 2 * n * b * Heaviside( x - b ) * x * a + 2 * n * a * Heaviside( x - a ) * x * b + Heaviside( -d + x ) * d ** 3 + 2 * d * Heaviside( -d + x ) * x * b - n * Heaviside( x - a ) * x ** 2 * b + n * Heaviside( x - a ) * x ** 2 * d - n * Heaviside( x - a ) * a ** 2 * b + n * Heaviside( x - a ) * a ** 2 * d + n * Heaviside( -d + x ) * x ** 2 * b + n * Heaviside( -d + x ) * d ** 2 * b - n * a * Heaviside( -d + x ) * d ** 2 - n * Heaviside( x - b ) * x ** 2 * d + n * Heaviside( x - b ) * x ** 2 * a - n * Heaviside( x - b ) * b ** 2 * d + n * Heaviside( x - b ) * b ** 2 * a - n * Heaviside( -d + x ) * x ** 2 * a - 2 * d * Heaviside( x - a ) * x * b ) / ( -d + a ) / ( -n * b + a + n * a - d ) / ( b - d )

def Dirac( x, sigma ):
    from scipy import logical_and, pi, cos
    f = ( 1. / 2. / sigma ) * ( 1 + cos( pi * x / sigma ) )
    b = logical_and( x <= sigma, x >= -sigma )
    f = f * b
    return f

def fcdf( x, a, b, d, n ):
    return 2 * ( -n + 1 ) / ( -d + a ) / ( n * b - a - n * a + d ) * Heaviside( x - a ) * Heaviside( d - x ) + 2 * ( -d + n * a - n * x + x ) / ( -d + a ) / ( n * b - a - n * a + d ) * Dirac( x, a ) * Heaviside( d - x ) - 2 * ( -d + n * a - n * x + x ) / ( -d + a ) / ( n * b - a - n * a + d ) * Heaviside( x - a ) * Dirac( x, d ) - 2 * n / ( b - d ) / ( n * b - a - n * a + d ) * Heaviside( x - d ) * Heaviside( b - x ) + 2 * n * ( b - x ) / ( b - d ) / ( n * b - a - n * a + d ) * Dirac( x, d ) * Heaviside( b - x ) - 2 * n * ( b - x ) / ( b - d ) / ( n * b - a - n * a + d ) * Heaviside( x - d ) * Dirac( x, b )

bd = 40
bh = 100

plt.figure( 1 )
plt.plot( x1, pdf( x1, 0, 0.06, 0.005, .01 ) )
plt.hist( data1, bins=bd, normed=1 )
plt.plot( x1, rv1.pdf( x1 ) )
plt.plot( x1, rv4.pdf( x1, 0.003, .03, 300 ) )

plt.figure( 11 )
plt.plot( x1, cdf( x1, 0, 0.06, 0.005, .01 ) )
plt.hist( data1, bins=bh, normed=1, cumulative=1 )
plt.plot( x1, rv1.cdf( x1 ) )
plt.plot( x1, rv4.cdf( x1, 0.003, .03, 300 ) )

plt.figure( 2 )
plt.plot( x2, pdf( x2, 0, 100, 55, 1 ) )
plt.hist( data2, bins=bd, normed=1 )
plt.plot( x2, rv2.pdf( x2 ) )
plt.plot( x2, rv4.pdf( x2, 2., 100., 0.03 ) )

plt.figure( 22 )
plt.plot( x2, cdf( x2, 0, 100, 55, 1 ) )
plt.hist( data2, bins=bh, normed=1, cumulative=1 )
plt.plot( x2, rv2.cdf( x2 ) )
plt.plot( x2, rv4.cdf( x2, 2., 100., 0.03 ) )

plt.figure( 3 )
x = linspace( 0, 6000, 1000 )
plt.plot( x, pdf( x, 0, 5000, 100, .01 ) )
plt.hist( data3, bins=bd, normed=1 )
plt.plot( x3, rv3.pdf( x3 ) )
plt.plot( x3, rv4.pdf( x3, 100., 3000, 0.0065 ) )

plt.figure( 33 )
plt.plot( x, cdf( x, 0, 5000, 100, .01 ) )
plt.hist( data3, bins=bh, normed=1, cumulative=1 )
plt.plot( x3, rv3.cdf( x3 ) )
plt.plot( x3, rv4.cdf( x3, 100., 3000., 0.0065 ) )



plt.show()

