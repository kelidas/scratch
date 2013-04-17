'''
Created on 19.10.2010

@author: Vasek
'''

from multiprocessing import Process
from numpy import sqrt, array


def thread( c, n ):
    for i in range( 0, n + 1 ):
        ret = 3 * sqrt( float( i ) * n * n )
    print 'thread', c, 'finished'
    print ret

if __name__ == '__main__':

    thr = []
    var = array( [1000000, 10000, 100] )
    for n, i in enumerate( var ):
        thr.append( Process( target = thread,
                        args = ( [n, i ] ) ) )

    for i in range( 3 ):
        thr[i].start()

#
#    for i in range( 0, 1000000 ):
#        sqrt( i + 5 * i )
#    print 'end #########################'


