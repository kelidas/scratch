'''
Created on 20.10.2010

@author: Vasek
'''
from multiprocessing import Pool, Queue, RawArray, Lock, Pipe
import time
#from multiprocessing.sharedctypes import Value, Array
from scipy.weave import \
    inline, converters
from numpy import zeros



n_ii = 10000


def my_inline( *args ):   
    arr = zeros( n_ii )
    conv = converters.default #blitz
    kwds = {'arg_names' : ['n_ii', 'arr'], 'local_dict' : {'n_ii':n_ii, 'arr':arr }, 'verbose' :0} 
    inline( args[0], type_converters=conv, compiler='mingw32', **kwds )
    #for i in range( len( args[1] ) ):
    #    args[1][i] = arr[i]
    args[1][:] = arr
    #print arr
    #print 'ARR', args[1][:]
    
def main():
    ARR1 = RawArray( 'd', zeros( n_ii ) )
    ARR2 = RawArray( 'd', zeros( n_ii ) )
    from multiprocessing import Process
    proc = Process( target=my_inline, args=[C_code1, ARR1] )
    proc2 = Process( target=my_inline, args=[C_code2, ARR2] )
    print 'start'
    start = time.time()
    proc.start()
    proc2.start()
    proc.join()
    from numpy import array
    arrc = array( ARR1[:] )
    proc2.join()
    arrc += array( ARR2[:] )
    print 'main time', time.time() - start
    print 'ARR complete', arrc

def main_one():
    ARR3 = RawArray( 'd', zeros( n_ii ) )
    from multiprocessing import Process
    proc = Process( target=my_inline, args=[C_code, ARR3] )
    print 'start'
    start = time.time()
    proc.start()
    proc.join()
    from numpy import array
    arrc = array( ARR3[:] )
    print 'main time', time.time() - start
    print 'ARR complete', arrc
    


#inline( C_code, arg_names = ['n_ii', 'arr'], local_dict = {'n_ii':n_ii, 'arr':arr }, type_converters = conv, verbose = 0 )

if __name__ == '__main__':
    
    C_code = '''
    for( int ii = 0; ii < 1000000; ii++){
        for( int ii = 0; ii < n_ii; ii++){
            *(arr + ii) = ii * ii;
        };};
    '''

    C_code1 = '''
    for( int ii = 0; ii < 1000000; ii++){
        for( int ii = 0; ii < n_ii/2.; ii++){
            *(arr + ii) = ii * ii;
        };};
    '''
    C_code2 = '''
    for( int ii = 0; ii < 1000000; ii++){
        for( int ii = n_ii/2.; ii < n_ii; ii++){
            *(arr + ii) = ii * ii;
        };};
    return_val = arr;
    '''
    
    #main()
    main_one()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    pool = Pool( processes = 4 )
#    n_ii = 10000
#    arr = zeros( n_ii )
#    conv = converters.blitz #blitz

#    import myglobals # anything (empty .py file)
#    arr = myglobals.data = zeros( n_ii )
#    a = "C_code, arg_names = ['n_ii', 'arr'], local_dict = {'n_ii':n_ii, 'arr':arr }, type_converters = conv, verbose = 0"
#    result = pool.apply_async( inline, args = ( C_code1, ), kwds = {'arg_names' : ['n_ii', 'arr'], 'local_dict' : {'n_ii':n_ii, 'arr':arr }, 'verbose' :0} )
#    #, kwds = {'arg_names' : ['n_ii', 'arr'], 'local_dict' : {'n_ii':n_ii, 'arr':arr } }
#    #result.get()
#    result.get()
#    print arr



#  funguje skoro



#def f( x ):
#    time.sleep( 5 )
#    return x * x
#
#if __name__ == '__main__':
#    pool = Pool( processes = 4 )              # start 4 worker processes
#
#    result = pool.apply_async( f, ( 10, ) )    # evaluate "f(10)" asynchronously
#    print result.get( timeout = 10 )           # prints "100" unless your computer is *very* slow
#
#    print pool.map( f, range( 10 ) )          # prints "[0, 1, 4,..., 81]"
#
#    it = pool.imap( f, range( 10 ) )
#    print it.next()                       # prints "0"
#    print it.next()                       # prints "1"
#    print it.next( timeout = 1 )              # prints "4" unless your computer is *very* slow
#
#    print 'konec'
#
#    import time
#    result = pool.apply_async( time.sleep, ( 10, ) )
#    print result.get( timeout = 1 )           # raises TimeoutError
