'''
Created on 19.10.2010

@author: Vasek
'''
from threading import Thread
from numpy import sqrt, array


def thread( c, n ):
    for i in range( 0, n + 1 ):
        ret = 3. * sqrt( float( i ) * n * n )
    print 'thread', c, 'finished', n
    print ret

thr = []
var = array( [1000000, 10000, 100] )
for n, i in enumerate( var ):
    thr.append( Thread( target = thread,
                    args = [n, i] ) )


for i in range( 0, 3 ):
    thr[i].start()

print 'end'
