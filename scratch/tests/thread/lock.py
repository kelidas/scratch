'''
Created on Oct 21, 2010

@author: kelidas
'''
from multiprocessing import Process, Lock
import time

def f( l, i ):
    l.acquire()
    for ii in xrange( 100 ):
        for ii  in xrange( 100 ):
            pass
    print 'hello world', i
    time.sleep( 1 )
    l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range( 10 ):
        Process( target = f, args = ( lock, num ) ).start()

    print 'ahoj'
