##from decimal import Decimal
#from traits.api import HasStrictTraits, Int, Instance, List, Regex, \
#    Str, HasTraits, Bool, HasTraits, Float, Property, cached_property, Class, \
#    Instance, List, on_trait_change, Int, Tuple, Bool, DelegatesTo, Event, Enum, \
#    implements, Str, Any, Trait, Interface, Either, Array
from numpy import cos, array, linspace, sin, sqrt, arange, sign
#    vstack, concatenate, where, argwhere, hstack, zeros, all, sin, cos, max, argmax, \
#    argmin, trapz, sign, sort, ogrid, sum, ones, expand_dims, searchsorted, nonzero, \
#    ravel, frompyfunc, ndarray, array_split, dsplit, hsplit, expand_dims, newaxis, \
#    indices, log, exp, reshape, arccos, mean
#from numpy.stats.spirrid.numeric import ones
#from numpy.random import randn, rand
#from scipy.interpolate import interp1d
#from scipy.stats import norm
#import matplotlib.pyplot as plt
#from scipy.stats import gamma as gamma_distr, norm, weibull_min, uniform, beta
#from math import e, pi
#from scipy.special import gamma, gammaln

from matplotlib import pyplot as plt
from math import pi, e

def H( x ):
    return sign( sign( x ) + 1.0 )

E = 200e3
d = 0.175
r = d / 2
A = r ** 2 * 3.1415
tau = 6. * d * pi
l = 17.0
#phi = 0.
z = 0.0
f = 0.03

def pullout( w, z, phi ):
    le = l / 2. - z / cos( phi ) * H( l / 2. - z / cos( phi ) )
    d = sqrt( E * A * tau * w ) * e ** ( f * phi )
    p = tau * le * e ** ( f * phi )
    return d * H( p - d ) + p * H( d - p )

def spirrid( w ):
    mean = 0.0
    r2 = 0.0
    for z in linspace( 0., l / 2., 100 ):
        for phi in linspace( 0, pi / 2 - 0.0000001, 100 ):
            m = pullout( w, z, phi ) * ( 2. / l ) * sin( phi ) * pi / 200. * l / 200.
            var = ( pullout( w, z, phi )  )** 2 * ( 2. / l ) * sin( phi ) * pi / 200. * l / 200.
            mean += m    #contribution to the first raw moment
            r2   += var  #contribution to the second raw moment
    return mean, sqrt( r2 - mean**2 ) #first central moment and sqrt of the second central moment

w = linspace( 0., .3, 100 )
mean, stdev = spirrid( w )

plt.plot( w, mean, color = 'red', linewidth = 2 )
plt.plot( w, mean + stdev, color = 'black', linewidth = 1 )
plt.plot( w, mean - stdev, color = 'black', linewidth = 1 )
plt.show()

#plt.plot( [0.0, 0.0, 1.0], [0.0, tau, tau], color = 'black', linewidth = 2 )
#plt.title( 'bond law', size = 'xx-large' )
#plt.xlabel( 'slip [mm]', size = 'x-large' )
#plt.ylabel( 'shear stress [N/mm]', size = 'x-large' )
#plt.ylim( 0.0, 5.0 )

#w = linspace( 0., 1.0, 100 )
#plt.plot( w, pullout( w ), color = 'black', linewidth = 2 )
#plt.title( 'pullout', size = 'xx-large' )
#plt.xlabel( 'crack opening [mm]', size = 'x-large' )
#plt.ylabel( 'force [N]', size = 'x-large' )
#plt.ylim( 0.0, 40.0 )
#
#plt.show()


