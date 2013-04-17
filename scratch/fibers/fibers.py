
import numpy as np
import matplotlib.pyplot as p
from math import log, exp
from scipy.misc import comb
import os
import time

start_t = time.time()
filename = 'fibers=20,m=5'
if os.path.exists(filename + '.npy'):
    data = np.load( filename + '.npy' )
else:
    data = np.loadtxt( filename + '.txt', skiprows = 5, dtype = np.float64 )
    np.save( filename + '.npy', data )
print 'data loaded', data.shape, 'time =', time.time() - start_t

n_fib = 20 # number of n_fib
m = 5.
s = 1.

# number of slices
n = 60

y = data[:, 2]

def f( x ):
    return m * ( x / s ) ** m * np.exp( -( ( x / s ) ** m ) ) / x

def F( x ):
    return 1 - np.exp( -( ( x / s ) ** m ) )

def PDF( k, n, x ):
    res = comb( n, k ) * k * f( x ) * F( x ) ** ( k - 1 ) * ( 1 - F( x ) ) ** ( n - k )
    return res

def PDF_int( k, n, x ):
    x_arr = np.linspace( 1e-15, x, 1000 )
    return np.trapz( PDF( k, n, x_arr ), x_arr )

def CDF( k, n, x ):
    res = 0.0
    for j in range( k, n + 1 ):
        res += comb( n, j ) * F( x ) ** j * ( 1 - F( x ) ) ** ( n - j )
    return res

switch = 'PDF' # 'CDF'
def eval( k, n, x, w ):
    if w == 0:
        return 0.
    else:
        if switch == 'CDF':
            return CDF( k, n, x ) * w
        elif switch == 'PDF':
            return PDF_int( k, n, x ) * w
eval_vct = np.vectorize( eval )


# re-sort by the first column (lexsort)
ind = np.argsort( data[:, 0] ) #np.lexsort( ( data[:, 1], data[:, 0] ) ) #
data = data[ind]
print '--- Data re-sorted ---'

# min and max value of x-array
xmin, xmax = data[:, 0][0], data[:, 0][-1]
print 'min, max - ', xmin, xmax

log_dx = ( log( xmax ) - log( xmin ) ) / n
bounds = np.logspace( log( xmin ), log( xmax ), n + 1, endpoint = True, base = exp( 1 ) )
midpoints = np.exp( ( np.log( bounds[1:] ) + np.log( bounds[:-1] ) ) / 2. )
print midpoints


# choose k-values - bins
k_vals = []
for i in range( 0, n ):
    b_left = data[:, 0] < bounds[i + 1]
    b_right = data[:, 0] >= bounds[i]
    bin = b_left * b_right
    k_vals.append( data[:, 1][bin] )
    #print data[:,1][bin]
last = np.hstack( ( k_vals[-1], data[:, 1][data[:, 0] == bounds[n]] ) )
k_vals.pop( -1 )
k_vals.append( last )
#print len(k_vals)

# save k-values in bins to the file
outfile = open( 'k_in_bins.txt', 'w' )
outfile.write( 'mid\tn_k\t--k_values-->>\n' )
for i, mid in enumerate( midpoints ):
    outfile.write( '%f\t%d' % ( mid, len( k_vals[i] ) ) )
    for j in range( len( k_vals[i] ) ):
        outfile.write( '\t%d' % k_vals[i][j] )
    outfile.write( '\n' )

outfile.close()



weights = []
for k in k_vals:
    try:
        weights.append(np.bincount(k.astype('int'), minlength=n_fib + 1))
    except ValueError:
        weights.append( np.zeros( n_fib + 1 ) )
weights = np.array( weights )

F_w = []
kk = np.arange( 0, n_fib + 1 )
for i, mid in enumerate( midpoints ):
    F_w.append( eval_vct( kk , n, mid, weights[i, :] ) / np.sum( weights[i, :] ) )


outfile = open( 'weights', 'w' )
outfile.write( 'bin\t\t--n_fiber-->>\n\t' )
for j in range( n_fib + 1 ):
    outfile.write( '\t%d' % j )
outfile.write( '\n' )
for i, mid in enumerate( midpoints ):
    outfile.write( '%d\t%f' % ( i + 1, midpoints[i] ) )
    for j in range( n_fib + 1 ):
        outfile.write( '\t%d' % weights[i, j] )
    outfile.write( '\t%d\t%f' % ( np.sum( weights[i, :] ), np.sum( F_w[i] ) ) )
    outfile.write( '\n' )

outfile.close()


# plot histogram of the slice
#p.figure()
#width = 1
#p.bar( np.arange( n_fib + 1 ) + 0.5, weights[16, :], width, fc = 'none' )
#p.xlim( -.5, n_fib + 1 + 0.5 )




p.figure()
p.loglog( midpoints, np.sum( np.array( F_w ), axis = 1 ), 'b-x' )
p.loglog( data[:, 0], y )#data[:, 2] )

p.figure()
x_arr = np.linspace( 1e-10, 3, 1000 )
p.plot( x_arr, f( x_arr ), linewidth = 3 )
for i in range( 10 ):
    p.plot( x_arr, PDF( i + 1, 10, x_arr ), label = '%d' % ( i + 1 ) )
p.legend()

p.figure()
p.plot( x_arr, F( x_arr ), linewidth = 3 )
for i in range( 10 ):
    p.plot( x_arr, CDF( i + 1, 10, x_arr ), label = '%d' % ( i + 1 ) )
p.legend()

#p.figure()
#p.plot( bounds, np.ones( n + 1 ), 'ro' )
#p.plot( midpoints, np.ones( n ), 'bx' )
#
#p.figure()
#p.plot( data[:, 0], data[:, 2], 'bx' )
#
#p.figure()
#p.plot( data[:, 0], data[:, 1], 'bx' )


p.show()
