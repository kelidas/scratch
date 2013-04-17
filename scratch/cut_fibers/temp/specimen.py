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
from matplotlib.pyplot import plot, hist, show
from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                    log as ln, append, logspace, hstack, sign, trapz, sin, cos, \
                    ogrid, sort, nonzero, tanh, broadcast, ones_like, arange, ndarray, diff
from pylab import savefig, plot, show
from scipy.interpolate import interp1d
from scipy.optimize import brentq, newton
import scipy.interpolate

from matplotlib.figure import Figure                       
from matplotlib.axes import Axes                           
from matplotlib.lines import Line2D                        
from matplotlib.backends.backend_agg import FigureCanvasAgg
 
from numpy.random import rand
from numpy import arccos, matrix, sum, arange

def Heaviside( x ):
    return ( sign( x ) + 1.0 ) / 2.0

def cut( sx, lx, x ): #sx is the left fiber coordinate, lx is the horizontal length projection
    if sx <= x <= sx + lx:
        return 1
    else:
        return 0

func = frompyfunc( cut, 3, 1 )

# fiber length
lf = 10
# specimen dimensions
l_x = 500
l_y = 100
l_z = 30

# number of fibers
n = 1000
# number of sections
n_sec = 10000

    
v = []

# fibers uniformly distributed in specimen volume
cosO = 1 - rand( 1, n ) 
lx = lf * cosO
sx = l_x * rand( 1, n ) 
sy = l_y * rand( 1, n )
#sec = rand( 1, n_sec ) * l_x
sec = linspace( 0, l_x, n_sec )
for i in range( 0, n_sec ):
    vec_cut = func( sx, lx, sec[i] )
    v.append( sum( vec_cut ) )
    

    

# plot specimen with fibers
fig = Figure()  #figsize=[4, 4]
ax = Axes( fig, [.1, .1, .8, .8] )                              
fig.add_axes( ax )                
for i in range( 0, len( sx[0] ) ):                        
    l = Line2D( [sx[0][i] - lf / 2. * cosO[0][i], sx[0][i] + lf / 2. * cosO[0][i]], [sy[0][i], sy[0][i]] )#- lf / 2. * sin( arccos( cosO[0][i] ) )                          
    ax.add_line( l ) 
ax.set_xlim( 0, 500 )
ax.set_ylim( 0, 100 )
                                            
canvas = FigureCanvasAgg( fig )    
         
canvas.print_figure( "specimen.png" )   

# plot histogram
pdf, bins, patches = hist( v, 1000, normed=0 ) #, facecolor='green', alpha=1
#plot( sx, sy, 'rx' )   # centroids
#print sum( pdf * diff( bins ) )
show()
















print 'exit'
exit()

