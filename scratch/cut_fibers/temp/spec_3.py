'''
Created on 3.3.2010

@author: Vasek
'''

from traits.api import HasTraits, HasStrictTraits, Float, Property, cached_property, \
                                Instance, List, on_trait_change, Int, Tuple, Bool, \
                                DelegatesTo, Event, Enum, implements, Button, File, CFloat

from traitsui.api import \
    View, Item, Tabbed, VGroup, HGroup, ModelView, HSplit, VSplit
from traitsui.menu import OKButton
from math import exp, e, sqrt, log, pi
from matplotlib.figure import Figure
from matplotlib.pyplot import plot, hist, show, title
from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                    log as ln, append, logspace, hstack, sign, trapz, sin, cos, \
                    ogrid, sort, ones_like, nonzero, ones, tanh, broadcast, ones_like, arange, ndarray, diff, minimum
from pylab import savefig, plot, show
from scipy.interpolate import interp1d
from scipy.optimize import brentq, newton
import scipy.interpolate
from scipy.stats import binom

from matplotlib.figure import Figure                       
from matplotlib.axes import Axes                           
from matplotlib.lines import Line2D                        
from matplotlib.backends.backend_agg import FigureCanvasAgg
 
from numpy.random import rand
from numpy import arccos, matrix, sum, arange

def Heaviside( x ):
    return ( sign( x ) + 1.0 ) / 2.0

def cut( sx, lx, x ): #sx is the left fiber coordinate, lx is the horizontal length projection
    if sx - lx / 2. <= x <= sx + lx / 2.:
        return 1
    else:
        return 0

cut_func = frompyfunc( cut, 3, 1 )

lf = 1.
lc = 1.5

n = 1  # we rotate one fiber
n_spec = 100 # number of independent specimens (each of which is cut once and contains n fibers)
nsim = 10000
v = []
delta = 0.3 #* lc / 2.


for i in range( 0, nsim ):  # number of specimens
    vec_cut = 0
    for j in range( 0, n_spec ):
        cosO = rand( 1, n ) # technicky vzato ma byt 1 - rand()
        lx = lf * cosO # n...cisel
        sx = rand( 1, n ) * lc - lc / 2. 
        vec_cut += cut_func( sx, lx, delta )
    v.append( sum( vec_cut ) )
print v

#for k in range (0,len(volno[0])): 
#    print volno[0][k]
    
    
N = n_spec * n  


def prob( lc, lf, delta ):
    #type I
    if lf <= lc - 2. * delta:
        print "Varianta I or III"
        return lf / lc / 2
    #type II
    if lf > lc - 2. * delta:
        print "Varianta II"
        return 1 / 4. / lf / lc * ( lf ** 2 - 3 * lc ** 2 - 4 * delta * lf + 2 * lc * lf + 12 * lc * delta - 12 * delta ** 2 ) + ( lc - 2 * delta ) ** 2 / ( 2 * lf * lc )
    

p = prob( lc, lf, delta )
print p

rv = binom( N, prob( lc, lf, delta ) )
x = linspace( 0, N, N + 1 )
plot( x, nsim * rv.pmf( x ) )

# plot histogram
pdf, bins, patches = hist( v, N, normed=0 ) #, facecolor='green', alpha=1
#print pdf/float(nsim)
#plot( bins[:-1], pdf/float(nsim), 'rx' )   # centroids
#print sum( pdf * diff( bins ) )
title( "Specimen: lc=%.2f, lf=%.2f, delta=%.2f, p=%.5f" % ( lc, lf, delta, p ) )
show()
















print 'exit'
exit()

