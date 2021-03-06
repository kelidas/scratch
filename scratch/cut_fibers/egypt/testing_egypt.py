##from decimal import Decimal
#from traits.api import HasStrictTraits, Int, Instance, List, Regex, \
#    Str, HasTraits, Bool, HasTraits, Float, Property, cached_property, Class, \
#    Instance, List, on_trait_change, Int, Tuple, Bool, DelegatesTo, Event, Enum, \
#    implements, Str, Any, Trait, Interface, Either, Array
from numpy import cos, array, linspace, sin, sqrt, arange, sign, min
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

E = 200.e3
d = 0.3 # mm
r = d / 2
A = r ** 2 * pi
tau = 1.76 * d * pi
l = 17.0 # mm
L = 100 # mm
#phi = 0.
# x = 0.0
f = 0.03

def cut_indicator( x, phi ):
    if ( l / 2. * cos( phi ) - abs( x ) ) < 0:
        return 0
    else:
        return 1

    
def pullout( w, x, phi ):
    le = ( l / 2. - abs( x ) / cos( phi ) )
    return  pullout2( w, le, phi ) 


def pullout2( w, le, phi ):
    d = sqrt( E * A * tau * w ) * e ** ( f * phi )
    p = tau * le * e ** ( f * phi )
    return  ( d * H( p - d ) + p * H( d - p ) )


def spirrid( w ):   
    r1 = 0.0
    r2 = 0.0
    n = 150
    # integration region
    phi_min = 0
    phi_max = pi / 2.
    x_min = - l / 2.
    x_max = + l / 2.
    x_min = - L / 2.
    x_max = + L / 2.
    # differentials 
    dphi =  (phi_max - phi_min) / n
    dx = (x_max - x_min) / n
    prob = 0
    for phi in linspace( phi_min + dphi / 2. , phi_max - dphi / 2., n ):
        for x in linspace( x_min + dx / 2.  , x_max - dx/2. , n ):  
            q = pullout( w, x, phi ) * cut_indicator( x, phi ) # delete contribution of fibers that do not touch the crack plane
            ## ff = P(B|A) = P(B prunik A) / P(A), kde event A == rez
            ff = sin( phi ) / (x_max - x_min) # joint probability density
            p = 1/2.*l/L # probability of the event of intersection, the probability must be dependent on position of the cut (delta)
            ff /= p # correction for the event of intersection
            ff *= cut_indicator( x, phi ) # correction so that the probability over the region of interest integrates to one
            dF = ff * dx * dphi # probability differential
            m = q * dF
            var = ( q ** 2) * dF
            prob += dF
            r1 += m    #contribution to the first raw moment
            r2 += var  #contribution to the second raw moment
    print prob
    mean = r1 #the first central moment 
    stdv = sqrt( r2 - r1 ** 2 ) # sqrt of the second central moment
    return mean, stdv 


def spirrid2( w ):   
    # integral over all possible configurations that cross the crack plane
    # the variables are angle and embedded length
    mean = 0.0
    r2 = 0.0
    n = 150
    phic_min = 0
    phic_max = pi / 2.
    le_min = 0
    le_max = l / 2.
    dphic = (phic_max - phic_min) / n
    dle = (le_max - le_min) / n
    prob = 0
    for phic in linspace( phic_min + dphic / 2. , phic_max - dphic / 2., n ):
        for le in linspace( le_min + dle / 2. , le_max - dle / 2., n ):  
            q = pullout2( w, le, phic )
            ff = sin( 2 * phic ) * 2 / l  # joint probability density
            dF = ff * dphic * dle # probability differential
            m = q * dF
            var = q ** 2 * dF
            prob += dF
            mean += m    #contribution to the first raw moment
            r2 += var  #contribution to the second raw moment
    print prob
    return mean, sqrt( r2 - mean ** 2 ) #first central moment and sqrt of the second central moment

w = linspace( 0., .03, 500 )
mean, stdev = spirrid( w )
print mean[-1], stdev[-1] ** 2
plt.plot( w, mean, color='red', linewidth=2 )
plt.plot( w, mean + stdev, color='black', linewidth=1 )
plt.plot( w, mean - stdev, color='black', linewidth=1 )
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


