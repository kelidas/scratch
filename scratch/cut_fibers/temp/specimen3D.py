

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
                    copy, mean, average, arctan, transpose, ones, copy as ncopy, trapz
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

from fibers import Fibers, Specimen
from probability import probability_cut_nooverlaps

def cut_area( df, lf, cosphi ):
    if arccos( cosphi ) < arctan( ( lf ) / df ):
        return pi * df ** 2 / 4. / cosphi
    else:
        return df * lf / sin( arccos( cosphi ) ) 
cut_area_func = frompyfunc( cut_area, 3, 1 )


spec = Specimen()  
fib = Fibers()

n_sim = 1

u = []
v = []
w = []
cos_cut = matrix( [] )
v_vol_frac_A = []
u_sec = linspace( 0., spec.l_x / 2., spec.l_x * 1000 )#.0 * spec.l_x / 2. #[-l_x * 0.99 / 2. , -l_x / 3., 0., l_x / 3. , l_x * 0.99 / 2. ]
v_sec = linspace( 0., spec.l_y / 2., spec.l_y * 1000 )#.0 * spec.l_y / 2. #[-l_x * 0.99 / 2. , -l_x / 3., 0., l_x / 3. , l_x * 0.99 / 2. ]
w_sec = linspace( 0., spec.l_z / 2., spec.l_z * 1000 ) #.0 * spec.l_z / 2. #[-l_x * 0.99 / 2. , -l_x / 3., 0., l_x / 3. , l_x * 0.99 / 2. ]

for i in range( 0, n_sim ):
    sx, lx, sy, ly, sz, lz = fib.generate_fibers()

    for j in range( 0, len( u_sec ) ):
        u_cut = fib.cut_func( sx, lx, u_sec[j] )
        p_u = probability_cut_nooverlaps( spec.l_x, fib.lf, u_sec[j] )
        u.append( p_u )
    for k in range( 0, len( v_sec ) ):
        v_cut = fib.cut_func( sy, ly, v_sec[k] )
        p_v = probability_cut_nooverlaps( spec.l_y, fib.lf, v_sec[k] )
        v.append( p_v )
    for l in range( 0, len( w_sec ) ):
        w_cut = fib.cut_func( sz, lz, w_sec[l] )
        p_w = probability_cut_nooverlaps( spec.l_z, fib.lf, w_sec[l] )
        w.append( p_w )
print '\n', sum( u )
print sum( u )#trapz( u, u_sec )
print sum( v )
print sum( w )
#p = probability_cut_nooverlaps( spec.l_x, fib.lf, u_sec[-1] )
#bin_mean = fib.n * p
#bin_stdv = sqrt( bin_mean * ( 1 - p ) )
#bin_skew = ( 1 - 2 * p ) / bin_stdv
#
#
#
#print "sec:", u_sec[-1] # , "vec ", v
#print "    mean value = %.5f" % ( matrix( v ).mean() ), "\t|  stnd devia = %.5f" % ( matrix( v ).std() )      , "\t|  skewness   ", skew( v )
#print "    mean_binom = %.5f" % bin_mean              , "\t|  stdv_binom = %.5f" % bin_stdv                   , "\t|  skew_binom ", bin_skew




# Enthought library imports
from mayavi.scripts import mayavi2
from mayavi.sources.array_source import ArraySource
from mayavi.modules.outline import Outline
from mayavi.modules.image_plane_widget import ImagePlaneWidget


def make_data( x, y, z ):
    """Creates some simple array data of the given dimensions to test
    with."""
    
    x = x.astype( 'f' )
    y = y.astype( 'f' )
    z = z.astype( 'f' )
    arr_list = [x, y, z]
    n_arr = len( arr_list )
    ogrid = []
    for i, arr in enumerate( arr_list ):
        shape = ones( ( n_arr, ), dtype='int' )
        shape[i] = len( arr )
        arr_i = ncopy( arr ).reshape( tuple( shape ) )
        ogrid.append( arr_i )
    x, y, z = ogrid
               
    scalars = x * z * y #(numpy.sin(x*y*z)/(x*y*z))
    # The copy makes the data contiguous and the transpose makes it
    # suitable for display via tvtk.  Please note that we assume here
    # that the ArraySource is configured to not transpose the data.
    s = transpose( scalars ).copy()
    # Reshaping the array is needed since the transpose messes up the
    # dimensions of the data.  The scalars themselves are ravel'd and
    # used internally by VTK so the dimension does not matter for the
    # scalars.
    s.shape = s.shape[::-1]
    
    return s

data = make_data( array( u ), array( v ), array( w ) )
print '\n', sum( data )

@mayavi2.standalone
def view_numpy( data ):
    """Example showing how to view a 3D numpy array in mayavi2.
    """
    # 'mayavi' is always defined on the interpreter.
    mayavi.new_scene()
    # Make the data and add it to the pipeline.
    
    src = ArraySource( transpose_input_array=False )
    src.scalar_data = data    
    mayavi.add_source( src )
    # Visualize the data.
    o = Outline()
    mayavi.add_module( o )
    ipw = ImagePlaneWidget()
    mayavi.add_module( ipw )
    ipw.module_manager.scalar_lut_manager.show_scalar_bar = True

    ipw_y = ImagePlaneWidget()
    mayavi.add_module( ipw_y )
    ipw_y.ipw.plane_orientation = 'y_axes'

    
if __name__ == '__main__':
    view_numpy( data )


exit()

# plot specimen with fibers
fig = figure( 0 )  #figsize=[4, 4] #Figure
ax = Axes3D( fig, [.1, .1, .8, .8], azim=90, elev=90 ) 

fig.add_axes( ax )          
for i in range( 0, len( sx[0] ) ):                        
    l = Line3D( [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
                 [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
                  [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]], \
                  linewidth=.5 )     
    #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
    #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
    #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
    ax.add_line( l ) 

ax.set_xlim3d( -l_x / 2., l_x / 2. )
ax.set_ylim3d( -l_y / 2., l_y / 2. )
ax.set_zlim3d( -l_z / 2., l_z / 2. )
ax.set_xlabel( 'X' )
ax.set_ylabel( 'Y' )
ax.set_zlabel( 'Z' )

                                         
#canvas = FigureCanvasAgg( fig )    
         
#canvas.print_figure( "specimen3D.png" )   
    

# plot histogram
figure( 1 )
delta = 0.
p = probability_cut_nooverlaps( l_x, lf, delta )

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






show()




print 'exit'
exit()

