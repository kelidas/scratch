
from stats.spirrid import SPIRRID
from matplotlib import pyplot as plt
from quaducom.pullout.constant_friction_finite_fiber import ConstantFrictionFiniteFiber
from math import pi, factorial
from itertools import combinations, chain


def choose( n, k ):
    '''
        Combination coefficient
    '''
    return factorial( n ) / ( factorial( k ) * factorial( n - k ) )

def powerset( iterable, par='all' ):
    '''
        Return object of all combination of iterable. 
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    '''
    s = list( iterable )
    if par == 'all':
        return chain.from_iterable( combinations( s, r ) for r in range( len( s ) + 1 ) )
    else:
        return combinations( s, par )

def run():
    # Quantities for the response function
    # and randomization

    # construct a default response function for a single filament
    dict_var = {'fu':1200.0e6,
                'qf':1500.,
                'L':0.02,
                'A':5.30929158457e-10,
                'E_mod':70.0e9,
                'z':0.0,
                'phi':0.,
                'f':0.0}
        
    outfile = open( 'pullout_comb_stat.dat', 'w' )
    
    comb = 0
    while_cond = 1
    while while_cond == 1: #for comb in range( 1, n_com + 1 ):
        comb += 1
        for i in range( 0, 2 ):
            # construct a default response function for a single filament
            rf = ConstantFrictionFiniteFiber()
            rf.set( **dict_var ) 

            # construct the integrator and provide it with the response function.
        
            s = SPIRRID( rf=rf,
                         min_eps=0.00, max_eps=0.05, n_eps=80 )
        
            # construct the random variables
        
            n_int = 10
        
            dict_rv = {
                       'fu':{'variable':'fu', 'distribution':'weibull_min', 'loc':1200.0e6, 'scale':200., 'n_int':n_int },
                       'qf':{'variable':'qf', 'distribution':'uniform', 'loc':1500., 'scale':100., 'n_int':n_int },
                       'L':{'variable':'L', 'distribution':'uniform', 'loc':0.02, 'scale':rf.L / 2., 'n_int':n_int},
                       'A':{'variable':'A', 'distribution':'uniform', 'loc':5.30929158457e-10, 'scale':.03 * 5.30929158457e-10, 'n_int':n_int },
                       'E_mod':{'variable':'E_mod', 'distribution':'uniform', 'loc':70.e9, 'scale':250.e9, 'n_int':n_int},
                       'z':{'variable':'z', 'distribution':'uniform', 'loc':0., 'scale':.03, 'n_int':n_int },
                       'phi':{'variable':'phi', 'distribution':'cos_distr', 'loc':0., 'scale':1., 'n_int':n_int},
                       'f':{'variable':'f', 'distribution':'uniform', 'loc':0., 'scale':.03, 'n_int':n_int },
                       }

            n_var = len( dict_rv )
            n_com = 0
            for k in range( 6, 7 ):
                n_com += choose( n_var, k )
                
            # end of the while loop
            if comb == n_com:
                while_cond = 0
                
            list_rv_comb = list( powerset( dict_rv, par=6 ) )

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
                          'compiled_QdG_loop'  : True,
                          'compiled_eps_loop' : True },
                          'go-',
                          '$\mathrm{C}_{e,\\theta} ( q(e,\\theta) \cdot G[\\theta] ) $ - %4.2f sec',
                          ),
                        ( 
                         {'cached_dG'         : True,
                          'compiled_QdG_loop'  : False,
                          'compiled_eps_loop' : False },
                         'b--',
                         '$\mathrm{P}_{e} ( \mathrm{N}_{\\theta} ( q(e,\\theta) \cdot G[\\theta] ) ) $ - %4.2f sec'
                         ),
                        ]
            
            print 'Combination', list_rv_comb[comb], ' -- ', i
            outfile.write( "Combination %s -- %i\n" % ( list_rv_comb[comb], i ) )
            outfile.write( "%s \t %s\n" % ( "Run", "Time" ) )
            
            for idx, run in enumerate( run_list ):
                run_options, plot_options, legend_string = run
                print 'run', idx,
                s.set( **run_options )
                plt.figure( comb )
                s.mean_curve.plot( plt, plot_options, linewidth=2, label=legend_string % s.exec_time )
                print 'execution time', s.exec_time, s.mu_q_peak
                outfile.write( "%s \t %s\n" % ( idx, s.exec_time ) )
            
            outfile.write( "=================\n" )
        
            plt.xlabel( 'strain [-]' )
            plt.ylabel( 'stress' )
            plt.legend( loc='lower right' )
        
            plt.title( s.rf.title )
            del s
    plt.show()

if __name__ == '__main__':
    run()

