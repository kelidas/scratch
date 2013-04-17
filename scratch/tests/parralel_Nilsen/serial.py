import numpy as np

def func( x, a = 0, b = 0, c = 1 ):
    return a * x ** 2 + b * x + c


def solve_problem( initialize, func, finalize ):
    input_args = initialize()
    output = [func( *args, **kwargs ) for args, kwargs in input_args]
    finalize( output )


class Parabola:
    def __init__( self, m, n, L ):
        self.m, self.n, self.L = m, n, L

    def initialize( self ):
        x = np.linspace( 0, self.L, self.n )
        a_values = np.linspace( -1, 1, self.m )
        b_values = np.linspace( -1, 1, self.m )
        c = 5

        self.input_args = []
        for a in a_values:
            for b in b_values:
                func_args = ( [x], {'a':a, 'b':b, 'c':c} )
                self.input_args.append( func_args )
        return self.input_args

    def func( self, x, a = 0, b = 0, c = 1 ):
        return a * x ** 2 + b * x + c

    def finalize( self, output_list ):
        self.ab = []
        for input, result in zip( self.input_args, output_list ):
            if min( result ) < 0:
                self.ab.append( ( input[1]['a'], input[1]['b'] ) )



if __name__ == '__main__':
    par = Parabola( 100, 50, 10 )
    solve_problem( par.initialize, par.func, par.finalize )

