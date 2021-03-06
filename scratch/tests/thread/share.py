'''
Created on Oct 21, 2010

@author: kelidas
'''
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double

class Point( Structure ):
    _fields_ = [( 'x', c_double ), ( 'y', c_double )]

def modify( n, x, s, A ):
    n.value **= 2
    s.value = s.value.upper()



if __name__ == '__main__':
    lock = Lock()

    n = Value( 'i', 7 )
    x = Value( c_double, 1.0 / 3.0, lock = False )
    s = Array( 'c', 'hello world', lock = lock )
    A = Array( 'd', [] ) #Array( Point, [( 1.875, -6.25 ), ( -5.75, 2.0 ), ( 2.375, 9.5 )], lock = lock )

    p = Process( target = modify, args = ( n, x, s, A ) )
    p.start()
    p.join()

    print n.value
    print x.value
    print s.value
    print [a for a in A]
