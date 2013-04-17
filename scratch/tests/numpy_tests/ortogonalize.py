from numpy import ones, copy as ncopy



def orthogonalize( arr_list ):
    '''Orthogonalize a list of one-dimensional arrays.
    '''
    n_arr = len( arr_list )
    ogrid = []
    for i, arr in enumerate( arr_list ):
        shape = ones( ( n_arr, ), dtype='int' )
        print 'shape = ', shape
        shape[i] = len( arr )
        print 'shape = ', shape
        arr_i = ncopy( arr ).reshape( tuple( shape ) )
        print 'arr_i = ', arr_i
        ogrid.append( arr_i )
        print 'ogrid ', ogrid
        
    return ogrid


print orthogonalize( ( [1, 2, 3], [5, 4, 8] ) )
