

#from math import cos, pi
from numpy import array, arange, ones_like, cos, pi, savetxt
from numpy.linalg import eig, eigvalsh, eigh, eigvals

N = 10

def A( i, j, n ):
    return ( -1 ) ** ( i - j + 1 ) * 2 / ( n - 2 ) * cos( pi * ( i - j ) / n )


ii = arange( 1, N + 1, 1 ).reshape( N, 1 )
jj = ones_like( ii ).reshape( 1, N )

i = ii * jj
j = ii.T * jj.T

a = A( i, j, N )
for idx in range( 0, N ):
    a[idx, idx] = 1





#print eig( a )[0]

P = A( i, j, N )
for idx in range( 0, N ):
    P[idx, idx] = 1

JC = A( N - i + 1, j, N )
Q = P - JC
Q = Q[0:N / 2, 0:N / 2]
print 'eigen values', eig( Q )[0]
print 'eigen vectors', eig( Q )[1]

print 'eigen values', eigh( Q )[0]
print 'eigen vectors', eigh( Q )[1]
print Q
savetxt( 'mat.txt', eigh( Q )[1] )

import matplotlib.pyplot as plt
x = arange( 1, N / 2. + 1, 1 )
plt.plot( x, eig( Q )[1].T )
plt.show()
