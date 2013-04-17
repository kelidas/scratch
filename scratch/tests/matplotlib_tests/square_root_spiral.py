
import matplotlib.pyplot as plt
from numpy import arctan, sqrt, cos, sin, pi, linspace

def phi_n( n ):
    return arctan( 1 / sqrt( n ) )

plt.figure( 0 )
phi = 0
x2 = 0
y2 = 0
for i in range( 1, 17 ):
    x1 = cos( phi ) * sqrt( i )
    y1 = sin( phi ) * sqrt( i )
    plt.plot( [0, x1], [0, y1] )
    plt.text( x1, y1, '$\sqrt{%i}$' % i )
    plt.plot( [x1, x2], [y1, y2] )
    phi += phi_n( i )
    x2 = x1
    y2 = y1
    
# Archimedian spiral
plt.figure( 1 )
plt.polar()
theta = linspace( 0, pi * 5, 200 )
a = 0.
b = .8
for thet in theta:
    plt.plot( thet, thet, 'r+' )
    plt.plot( thet + 10, a + b * thet, 'b+' )
plt.show()
