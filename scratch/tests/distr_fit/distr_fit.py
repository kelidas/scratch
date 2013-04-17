from traits.api import HasTraits, Float, Property, \
    cached_property, Event, Array, Instance, List
from scipy import stats
from scipy.optimize import fsolve
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def plothist( x, distfn, loc, scale, args=[], bins=10 ):
    plt.figure()
    n, bins, patches = plt.hist( x, bins, normed=1, facecolor='green', alpha=0.75 )
    maxheight = max( [p.get_height() for p in patches] )
    yt = distfn.pdf( bins, loc=loc, scale=scale, *args )
    lt = plt.plot( bins, yt, 'b-', linewidth=2 )
    ymax = np.max( [maxheight, np.max( yt )] ) * 1.1
    plt.ylim( 0, ymax )
    plt.xlabel( 'Smarts' )
    plt.ylabel( 'Probability' )
    plt.title( r'$\mathrm{Testing: %s :}\ \mu=%f,\ \sigma=%f$' % ( distfn.name, loc, scale ) )
  
    plt.grid( True )
    plt.draw()
    
#plothist( np.linspace( 0, 10, 100 ), stats.norm, 2, 2, bins=10 )
#plt.show()


targetdist = ['norm', 'beta', 'chi2', 'cosine', 'expon', 'exponweib', 'exponpow',
              'weibull_min', 'weibull_max', 'gamma', 'gumbel_r', 'gumbel_l',
              'invnorm', 'invweibull', 'logistic', 'loggamma', 'lognorm', 't',
              'pareto', 'powerlaw', 'powerlognorm', 'powernorm',
              'rayleigh', 'triang', 'uniform',
              'binom', 'bernoulli', 'poisson']
targetdist = ['norm', 'uniform', 'triang']#, 'lognorm'

class Fit( HasTraits ):
    targetdist = ['norm', 'uniform', 'triang']
    distribution = List( targetdist )
    data = Array()

    # TODO __call__
    def dist_fit( self ):
        """ Fit all of the target distributions """
        fitted = []
        for distr in self.distributions:
            print 'fitting distr', distr.name
            distfn = getattr( stats, distr )
            sm = self.data.mean()
            sstd = self.data.var()
            #par_est = tuple( distfn.fit( self.data, loc=sm, scale=sstd ) )
            loc, scale = distfn.est_loc_scale( self.data )

            fitted.append( distr )
            print 'fit', par_est
            arg_est = par_est[:-2]
            loc_est = par_est[-2]
            scale_est = par_est[-1]
            ks_stat, ks_pval = stats.kstest( rvs_normed, distfn, arg_est )
            print 'kstest', ks_stat, ks_pval
        self.distributions = fitted
        
            
        print 'finished fitting'




if __name__ == '__main__':
    
    print 'exit'
