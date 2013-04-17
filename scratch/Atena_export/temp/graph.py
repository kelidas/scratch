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
from math import exp, e, sqrt, log, pi, floor
from matplotlib.figure import Figure
from matplotlib.pyplot import plot, hist, show
from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                    log as ln, append, logspace, hstack, sign, trapz, sin, cos, sqrt, \
                    ogrid, sort, nonzero, tanh, broadcast, ones_like, arange, ndarray, diff, \
                    copy, mean, average, arctan, ones, ones_like

from scipy.interpolate import interp1d
from scipy.optimize import brentq, newton
import scipy.interpolate

from matplotlib.figure import Figure                       
from matplotlib.axes import Axes                           
from matplotlib.lines import Line2D                        
from matplotlib.backends.backend_agg import FigureCanvasAgg
 
from numpy.random import rand
from numpy import arccos, matrix, sum, arange
from scipy.stats import binom, norm, skew

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d

from mpl_toolkits.mplot3d.art3d import Line3D
import matplotlib.pyplot as plt
import matplotlib.figure as fig
from matplotlib import rc



def x_lim(L, phi):
    return -L/2. * (1-cos(phi)), L/2. * (1-cos(phi))

def f_phi(phi):
    return sin(phi)

def f_x(L, phi):
    return 1./(L*(1-cos(phi)))#*ones_like(phi)

def H_lim(L, phi):
    return -L/2.*cos(phi), L/2.*cos(phi)

n=300+2

phi = linspace(0.02,pi/2.,n)
L = 1.


x_lim1, x_lim2 = x_lim(L, phi)
fphi = f_phi(phi)
fx = f_x(L, phi)
H_lim1, H_lim2 = H_lim(L, phi)

z = fx[1:-1]*fphi[1:-1]




plt.figure(0)
rc('font', family='serif', style='normal', variant='normal', stretch='normal')

plt.plot(phi, x_lim1)
plt.plot(phi, x_lim2)
plt.plot(phi, H_lim1)
plt.plot(phi, H_lim2)
plt.title('Nadpis grafu')

y=linspace(H_lim(L, 0)[0],H_lim(L, 0)[1],n-2)

fig = plt.figure(1)

ax = Axes3D(fig)
X, Y, Z = (phi[1:-1]*ones((n-2,1))).T, y*ones((n-2,1)), (z*ones((n-2,1))).T
#ax.plot3D(X.ravel(), Y.ravel(), Z.ravel(),'ro')  
#ax.contour3D(X, Y, Z)
ax.plot_wireframe(X, Y, Z,rstride=6,cstride=6, color='blue', linewidth=0.5)
#ax.plot_surface(X, Y, Z)
ax.plot(phi, x_lim1, zs=0, zdir='z', label='zs=0, zdir=z', color='red')
ax.plot(phi, x_lim2, zs=0, zdir='z', label='zs=0, zdir=z', color='red')
ax.plot(phi, H_lim1, zs=0, zdir='z', label='zs=0, zdir=z', color='green')
ax.plot(phi, H_lim2, zs=0, zdir='z', label='zs=0, zdir=z', color='green')
ax.plot3D(phi[1:-1], x_lim1[1:-1], z,'r-', linewidth=1.5)
ax.plot3D(phi[1:-1], x_lim2[1:-1], z,'r-', linewidth=1.5)
#ax.plot3D([0.,0.], [x_lim(L, 0.)[0],x_lim(L, 0)[1]], [0.,f_x(L, .1)],'r-')
ax.plot3D(phi[1:-1], H_lim1[1:-1], z,'g-', linewidth=1.5)
ax.plot3D(phi[1:-1], H_lim2[1:-1], z,'g-', linewidth=1.5)


#plt.savefig('C:\Documents and Settings\Vasek\Plocha\imag.eps')

### plot specimen with fibers
##fig = figure( 0 )  #figsize=[4, 4] #Figure
##ax = Axes3D( fig, [.1, .1, .8, .8], azim=90, elev=90 ) 
##
##fig.add_axes( ax )          
##for i in range( 0, len( sx[0] ) ):                        
##    l = Line3D( [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
##                 [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
##                  [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]], \
##                  linewidth=.5 )     
##    #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
##    #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
##    #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
##    ax.add_line( l ) 
##
##ax.set_xlim3d( -l_x / 2., l_x / 2. )
##ax.set_ylim3d( -l_y / 2., l_y / 2. )
##ax.set_zlim3d( -l_z / 2., l_z / 2. )
##ax.set_xlabel( 'X' )
##ax.set_ylabel( 'Y' )
##ax.set_zlabel( 'Z' )
##
##                                         
###canvas = FigureCanvasAgg( fig )    
##         
###canvas.print_figure( "specimen3D.png" )   
##    
##
### plot histogram
##figure( 1 )
##delta = 0.
##p = prob( l_x, lf, delta )
##
##rvb = binom( n, p )
##rvn = norm( n * p, sqrt( n * p * ( 1 - p ) ) )
##
##graph_from = floor( bin_mean - 4 * bin_stdv )
##graph_to = floor( bin_mean + 4 * bin_stdv ) + 1
##
##
##x = arange( graph_from , graph_to )
##plot( x, n_sim * rvb.pmf( x ) )
##plot( x, n_sim * rvn.pdf( x ) )
###plot( x, 20 * rv.pmf( x ) )
##
##pdf, bins, patches = hist( v, n_sim, normed=0 ) #, facecolor='green', alpha=1
###set_xlim( bin_mean - 2 * bin_stdv, bin_mean + 2 * bin_stdv )
###plot( sx, sy, 'rx' )   # centroids
###print sum( pdf * diff( bins ) )
##
###print v
####for i in range( 0, len( v ) ): 
####    print v[i]
###print "mean value ", matrix( v ).mean(), "binom ", n * p
###print "standard deviation", matrix( v ).std(), "binom ", sqrt( n * p * ( 1 - p ) )






plt.show()




print 'exit'


