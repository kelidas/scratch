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
                    copy, mean, average, arctan
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
from scipy.stats import binom, norm, skew

from mpl_toolkits.mplot3d import Axes3D 
from mpl_toolkits.mplot3d.art3d import Line3D
from matplotlib.pyplot import figure


def Heaviside( x ):
    return ( sign( x ) + 1.0 ) / 2.0

def cut( sx, lx, x ): #sx is the left fiber coordinate, lx is the horizontal length projection
    if ( sx - lx / 2. <= x )and( x <= sx + lx / 2. ):
        return 1
    else:
        return 0

func = frompyfunc( cut, 3, 1 )

def prob( lc, lf, delta ):
    #type I and III
    if ( lf <= lc / 2. - delta ) and ( lf <= lc / 2. + delta ):
        print "Varianta I or III ",
        return lc / lf * ( ln( lc / ( lc - lf ) ) ) - 1
    #type II
    if ( lf < lc / 2. + delta ) and ( lf > lc / 2. - delta ):
        print "Varianta II ",
        return 1 / 2. / lf * ( ( lc + 2. * delta ) * ln( 2. / ( lc + 2. * delta ) ) - ( ln( lc - lf ) + 1 ) * ( lc - 2. * delta ) + 2. * lc * ln( lc ) )
    #type IV
    if ( lf >= lc / 2. + delta ) and ( lf >= lc / 2. - delta ):
        print "Varianta IV ",
        return  1 + 1 / lf * ( -lc + ( lc / 2. - delta ) * ln( ( lc + 2 * delta ) / ( lc - 2 * delta ) ) + lc * ln( 2 * lc / ( lc + 2 * delta ) ) )

def cut_area( df, lf, cosphi ):
    if arccos( cosphi ) < arctan( ( lf ) / df ):
        return pi * df ** 2 / 4. / cosphi
    else:
        return df * lf / sin( arccos( cosphi ) ) 
cut_area_func = frompyfunc( cut_area, 3, 1 )


   

# fiber
lf = 2.
df = 23e-6
Af = pi * df ** 2 / 4.
Vf = Af * lf * 1e-2
# specimen dimensions
l_x = 10.
l_y = 10.
l_z = 10.
Vc = l_x * l_y * l_z * 1e-6
Ac = l_z * l_y * 1e-4

# number of fibers
n = 100
# number of sections
#n_sec = 10000
n_sim = 1

#sec = rand( 1, n_sec ) * l_x
v = []
cos_cut = matrix( [] )
v_vol_frac_A = []
sec = .0 * l_x / 2.#[-l_x * 0.99 / 2. , -l_x / 3., 0., l_x / 3. , l_x * 0.99 / 2. ]#linspace( 0, l_x, n_sec )

for j in range( 0, n_sim ):
    # fibers uniformly distributed in specimen volume
    cosphi_x = rand( 1, n ) # 1-rand(1,n)
    phi_x = arccos( cosphi_x )
    theta = rand( 1, n ) * 2. * pi
    costheta = cos( theta )
    sintheta = sin( theta )
    cosphi_y = sin( phi_x ) * sintheta 
    phi_y = arccos( cosphi_y )
    #print phi_y * 180 / pi
    cosphi_z = sin( phi_x ) * costheta 
    phi_z = arccos( cosphi_z )
    cos_cut = copy( cosphi_x )
    
    lx = abs( lf * cosphi_x )
    ly = abs( lf * cosphi_y )
    lz = abs( lf * cosphi_z )
    
    free_x = l_x - lx
    free_y = l_y - ly
    free_z = l_z - lz
    sx = free_x * rand( 1, n ) - free_x / 2.
    sy = free_y * rand( 1, n ) - free_y / 2.
    sz = free_z * rand( 1, n ) - free_z / 2.
    
    # rotation of cut fiber
    cos_cut *= func( sx, lx, sec )
    #print cos_cut[cos_cut != 0]
    #v_cos_cut.append( sum( cos_cut ) )
    vol_frac_A = mean( cut_area_func( df, lf * 1e-2, cos_cut[cos_cut != 0] ) ) #/ Ac * 100 
    v_vol_frac_A.append( vol_frac_A )
#    for i in range( 0, len( cos_cut[cos_cut != 0] ) ):
#        if arccos( cos_cut[cos_cut != 0][i] ) < arctan( lf * 1e-2 / df ):
#            v_vol_frac_A.append( Af / cos_cut[cos_cut != 0][i] )
#        else:
#            v_vol_frac_A.append( df * lf * 1e-2 / sin( arccos( cos_cut[cos_cut != 0][i] ) ) )
    
#    for i in range( 0, len( phi_x[0] ) ): 
#        print sx[0][i], lx[0][i]
    vec_cut = func( sx, lx, sec )
    v.append( sum( vec_cut ) )
    
p = prob( l_x, lf, sec )
bin_mean = n * p
bin_stdv = sqrt( bin_mean * ( 1 - p ) )
bin_skew = ( 1 - 2 * p ) / bin_stdv





vol_frac_V = Vf / Vc * 100 * n
 
vol_frac_A = mean( v_vol_frac_A ) / Ac * 100

print "sec:", sec # , "vec ", v
print "    mean value = %.5f" % ( matrix( v ).mean() ), "\t|  stnd devia = %.5f" % ( matrix( v ).std() )      , "\t|  skewness   ", skew( v )
print "    mean_binom = %.5f" % bin_mean              , "\t|  stdv_binom = %.5f" % bin_stdv                   , "\t|  skew_binom ", bin_skew
print "    vol_frac_V = %.3g%%" % vol_frac_V            , "\t|  vol_frac_A = %.3g%%" % vol_frac_A                 , "\t|  v_V /  v_A ", vol_frac_V / vol_frac_A
#print Af
#print Af / cos_cut[cos_cut != 0]

#for i in range( 0, len( cos_cut[0] ) ):
#    if cos_cut[0][i] != 0:
#        print cos_cut[0][i]



# 3D plot specimen with fibers
#fig = figure( 0 )  #figsize=[4, 4] #Figure
#ax = Axes3D( fig, [.1, .1, .8, .8], azim=90, elev=90 ) 
#
#fig.add_axes( ax )          
#for i in range( 0, len( sx[0] ) ):                        
#    l = Line3D( [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
#                 [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
#                  [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]], \
#                  linewidth=.5 )     
#    #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
#    #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
#    #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
#    ax.add_line( l ) 
#
#ax.set_xlim3d( -l_x / 2., l_x / 2. )
#ax.set_ylim3d( -l_y / 2., l_y / 2. )
#ax.set_zlim3d( -l_z / 2., l_z / 2. )
#ax.set_xlabel( 'X' )
#ax.set_ylabel( 'Y' )
#ax.set_zlabel( 'Z' )



fig2 = figure( 1 )
ax2 = Axes( fig2, [.1, .1, .8, .8] ) 

fig2.add_axes( ax2 )          
for i in range( 0, len( sx[0] ) ):                        
    l = Line2D( [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
                  [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]], \
                  linewidth=.5 )     
    #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
    #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
    #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
    ax2.add_line( l ) 
ax2.plot( sy, sz, 'ro' )
ax2.set_xlim( -6, 6. )
ax2.set_ylim( -6., 6. )
ax2.plot( [ -l_x / 2., l_x / 2. ], [l_y / 2., l_y / 2.], 'r-' )
ax2.plot( [ -l_x / 2., l_x / 2. ], [-l_y / 2., -l_y / 2.], 'r-' )
ax2.plot( [ l_x / 2., l_x / 2. ], [-l_y / 2., l_y / 2.], 'r-' )
ax2.plot( [ -l_x / 2., -l_x / 2. ], [-l_y / 2., l_y / 2.], 'r-' )


                                         
#canvas = FigureCanvasAgg( fig )    
         
#canvas.print_figure( "specimen3D.png" )   
    

# plot histogram
figure( 2 )
delta = 0.
p = prob( l_x, lf, delta )

rvb = binom( n, p )
rvn = norm( n * p, sqrt( n * p * ( 1 - p ) ) )

graph_from = floor( bin_mean - 4 * bin_stdv )
graph_to = floor( bin_mean + 4 * bin_stdv ) + 1


x = arange( graph_from , graph_to )
plot( x, n_sim * rvb.pmf( x ) )
plot( x, n_sim * rvn.pdf( x ) )
#plot( x, 20 * rv.pmf( x ) )

pdf, bins, patches = hist( v, n_sim, normed=0 ) #, facecolor='green', alpha=1
#set_xlim( bin_mean - 2 * bin_stdv, bin_mean + 2 * bin_stdv )
#plot( sx, sy, 'rx' )   # centroids
#print sum( pdf * diff( bins ) )

#print v
##for i in range( 0, len( v ) ): 
##    print v[i]
#print "mean value ", matrix( v ).mean(), "binom ", n * p
#print "standard deviation", matrix( v ).std(), "binom ", sqrt( n * p * ( 1 - p ) )
def pdf_x( L, l, delta, dv ):
    if - L / 2 + l / 2 + dv < delta < L / 2 - l / 2 - dv:
        return 2 * dv / l * ln( L / ( L - l ) )
    if  L / 2 - l / 2 - dv < delta < L / 2 - l / 2 + dv:
        return 1 / 2. + 1 / l * ( ( delta - dv ) * ln( L - l ) + ( delta + dv ) * ( 1 - ln( 2 * ( delta + dv ) ) ) + 2 * dv * ln( L ) - L / 2. )
    if ( delta > L / 2. - l / 2. + dv ) and ( delta > L / 2. - l / 2. - dv ):
        return 1 / l * ( 2 * dv * ( 1 + ln( L / 2. ) ) - ( delta + dv ) * ln( delta + dv ) + ( delta - dv ) * ln( delta - dv ) )
pdf_x_func = frompyfunc( pdf_x, 4, 1 )

figure( 3 )
div = 50.
xx = linspace( 0, l_x / 2., 1000 )
pdf, bins, patches = hist( sx[0], div, normed=0 )
plot( xx, pdf_x_func( l_x, lf, xx, l_x / div ) * n / 2., color='red', linewidth=4 )


show()




print 'exit'
exit()

