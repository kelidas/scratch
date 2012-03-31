
from stats.spirrid import SPIRRID
from matplotlib import pyplot as plt
from stats.spirrid.rf_filament import Filament
from math import pi, factorial
from itertools import combinations, chain

def choose( n, k ):
    '''
        Combination coefficient
    '''
    return factorial( n ) / ( factorial( k ) * factorial( n - k ) )

def powerset( iterable ):
    '''
        Return object of all combination of iterable. 
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    '''
    s = list( iterable )
    return chain.from_iterable( combinations( s, r ) for r in range( len( s ) + 1 ) )

def run():
    # Quantities for the response function
    # and randomization
    # 
    E_mod = 70 * 1e+9 # Pa
    sig_u = 1.25 * 1e+9 # Pa
    D = 26 * 1.0e-6 # m
    A = ( D / 2.0 ) ** 2 * pi
    xi_u = sig_u / E_mod
    
    dict_var = {'E_mod':70.e9,
                'xi':0.02,
                'A':A,
                'theta':0,
                'lambd':0}
        
    outfile = open( 'filament_comb_stat.dat', 'w' )
    
    comb = 0
    while_cond = 1
    while while_cond == 1: #for comb in range( 1, n_com + 1 ):
        comb += 1
        for i in range( 0, 2 ):
            # construct a default response function for a single filament
            rf = Filament()
            rf.set( **dict_var )

            # construct the integrator and provide it with the response function.
        
            s = SPIRRID( rf=rf,
                         min_eps=0.00, max_eps=0.05, n_eps=80 )
            
            # construct the random variables
        
            n_int = 32
        
            dict_rv = {
                       'xi':{'variable':'xi', 'distribution':'weibull_min', 'scale':0.02, 'shape':10., 'n_int':n_int},
                       'E_mod':{'variable':'E_mod', 'distribution':'uniform', 'loc':70e+9, 'scale':15e+9, 'n_int':n_int},
                       'theta':{'variable':'theta', 'distribution':'uniform', 'loc':0.0, 'scale':0.01, 'n_int':n_int},
                       'lambd':{'variable':'lambd', 'distribution':'uniform', 'loc':0.0, 'scale':.2, 'n_int':n_int},
                       'A':{'variable':'A', 'distribution':'uniform', 'loc':A * 0.3, 'scale':0.7 * A, 'n_int':n_int},
                       }
            
            n_var = len( dict_rv )
            n_com = 0
            for k in range( 0, n_var ):
                n_com += choose( n_var, k )
            print 'The only last combination'
            comb = n_com
            # end of the while loop
            if comb == n_com:
                while_cond = 0
                        
            list_rv_comb = list( powerset( dict_rv ) )
            for rv in list_rv_comb[comb]:
                s.add_rv( **dict_rv[rv] )
                
            # define a tables with the run configurations to start in a batch
        
            run_list = [
                        ( 
                         {'cached_dG'         : False,
                          'compiled_QdG_loop'  : True,
                          'compiled_eps_loop' : True },
                          'bx-',
                          '$\mathrm{C}_{e,\\theta} ( q(e,\\theta) \cdot g[\\theta_1]  g[\\theta_2] \dots g[\\theta_n] ) $ - %4.2f sec'
                         ),
                        ( 
                         {'cached_dG'         : False,
                          'compiled_QdG_loop'  : True,
                          'compiled_eps_loop' : False },
                         'r-2',
                         '$\mathrm{P}_{e} ( \mathrm{C}_{\\theta} ( q(e,\\theta) \cdot g[\\theta_1]  g[\\theta_2] \dots g[\\theta_n] ) ) $ - %4.2f sec',
                         ),
                         ( 
                         {'cached_dG'         : True,
                          'compiled_QdG_loop'  : False,
                          'compiled_eps_loop' : False },
                         'y--',
                         '$\mathrm{P}_{e} ( \mathrm{N}_{\\theta} ( q(e,\\theta) \cdot G[\\theta] ) ) $ - %4.2f sec'
                         ),
                        ( 
                         {'cached_dG'         : True,
                          'compiled_QdG_loop'  : True,
                          'compiled_eps_loop' : True },
                          'go-',
                          '$\mathrm{C}_{e,\\theta} ( q(e,\\theta) \cdot G[\\theta] ) $ - %4.2f sec',
                          ),
                        ]
        
            legend = []
        
            print 'Combination', list_rv_comb[comb], ' -- ', i
            outfile.write( "Combination %s -- %i\n" % ( list_rv_comb[comb], i ) )
            outfile.write( "%s \t %s\n" % ( "Run", "Time" ) )   
            
            for idx, run in enumerate( run_list ):
                run_options, plot_options, legend_string = run
                print 'run', idx,
                s.set( **run_options )
                plt.figure( comb )
                s.mean_curve.plot( plt, plot_options )
                print 'execution time', s.exec_time
                outfile.write( "%s \t %s\n" % ( idx, s.exec_time ) )
                legend.append( legend_string % s.exec_time )
                
            outfile.write( "=================\n" )
        
            plt.xlabel( 'strain [-]' )
            plt.ylabel( 'stress' )
            plt.legend( legend )
        
            plt.title( s.rf.title )
            
            del s
    plt.show()

if __name__ == '__main__':
    run()
