import matplotlib.pyplot as plt
from scipy.stats import hypergeom, rv_discrete
import numpy as np
numargs = hypergeom.numargs
#[ M, n, N ] = [100, 10, -1]

#Display frozen pmf:

rv = hypergeom( 10, 20, 3 )
print rv.dist.b
x = np.arange( 0, np.min( rv.dist.b, 3 ) + 1 )
h = plt.plot( x, rv.pmf( x ) )
exit()
#Check accuracy of cdf and ppf:

prb = hypergeom.cdf( x, M, n, N )
h = plt.semilogy( np.abs( x - hypergeom.ppf( prb, M, n, N ) ) + 1e-20 )

#Random number generation:

R = hypergeom.rvs( M, n, N, size=100 )

#Custom made discrete distribution:

vals = [np.arange( 7 ), ( 0.1, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1 )]
custm = rv_discrete( name='custm', values=vals )
h = plt.plot( vals[0], custm.pmf( vals[0] ) )

