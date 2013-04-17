from traits.api import HasTraits, HasStrictTraits, Float, Property, cached_property, \
                                Instance, List, on_trait_change, Int, Tuple, Bool, Array, \
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
                    copy, mean, average, arctan, min
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


class Specimen( HasTraits ):
    # specimen dimensions
    l_x = Float( 0.05, auto_set=False, enter_set=True ) # [m]
    l_y = Float( 0.05, auto_set=False, enter_set=True ) # [m]
    l_z = Float( 0.05, auto_set=False, enter_set=True ) # [m]
    
    def __init__( self, **kw ):
        super( Specimen, self ).__init__( **kw )
    
    def _get_volume( self ):
        return self.l_x * self.l_y * self.l_z
    def _get_cross_area( self ):
        return self.l_z * self.l_y

class Fibers( HasTraits ):
    spec = Instance( Specimen )
    
    # number of fibers
    n = Int( 100 ) 
    # fibers length
    lf = Float( .01 ) # [m]
    # fibers diameter
    df = Float( 0.001 ) #23e-6 # [m]
    overlaps = Bool( False )
    
    sim_i = Int( 0 )
    
    #if spec.l_x < lf or spec.l_y < lf or spec.l_z < lf:
    #    raise IOError( 'This configuration is not possible. Fiber length is larger than specimen dimension' )
    
    phi_x = Property( Array, depends_on='n, sim_i' )
    @cached_property
    def _get_phi_x( self ):
        #print 'jsem tu phi_x'
        # fibers uniformly distributed in specimen volume
        cosphi_x = rand( 1, self.n ) # 1-rand(1,self.n)
        return arccos( cosphi_x )
        
    theta = Property( Array, depends_on='n, sim_i' )
    @cached_property
    def _get_theta( self ):
        return rand( 1, self.n ) * 2. * pi
    
    phi_y = Property( Array, depends_on=['phi_x', 'theta'] )
    @cached_property
    def _get_phi_y( self ):
        cosphi_y = sin( self.phi_x ) * sin( self.theta )
        return arccos( cosphi_y )
    
    phi_z = Property( Array, depends_on=['phi_x', 'theta'] )
    @cached_property
    def _get_phi_z( self ):
        cosphi_z = sin( self.phi_x ) * cos( self.theta ) 
        return arccos( cosphi_z )
    
    lx = Property( Array , depends_on=['phi_x', 'lf'] )
    @cached_property
    def _get_lx( self ):
        return abs( self.lf * cos( self.phi_x ) )
    
    ly = Property( Array, depends_on=['phi_y', 'lf'] )
    @cached_property
    def _get_ly( self ):
        return abs( self.lf * cos( self.phi_y ) )
    
    lz = Property( Array, depends_on=['phi_z', 'lf'] )
    @cached_property
    def _get_lz( self ):
        return abs( self.lf * cos( self.phi_z ) )
        
    sx = Property( Array , depends_on=['n', 'overlaps', 'lx', 'spec'] )
    @cached_property
    def _get_sx( self ):
        spec = self.spec
        if self.overlaps == False:
            #print spec.l_x
            free_x = spec.l_x - self.lx
        else:
            free_x = spec.l_x
        return free_x * rand( 1, self.n ) - free_x / 2.
        
    sy = Property( Array, depends_on=['n', 'overlaps', 'ly'] )
    @cached_property
    def _get_sy( self ):
        spec = self.spec
        if self.overlaps == False:
            free_y = spec.l_y - self.ly
        else:
            free_y = spec.l_y
        return free_y * rand( 1, self.n ) - free_y / 2.
    
    sz = Property( Array, depends_on=['n', 'overlaps', 'lz'] )
    @cached_property
    def _get_sz( self ):
        spec = self.spec
        if self.overlaps == False:
            free_z = spec.l_z - self.lz
        else:
            free_z = spec.l_z
        return free_z * rand( 1, self.n ) - free_z / 2.
        

    
    def _get_volume( self ):
        # fibers volume
        return pi * self.df ** 2 / 4. * self.lf
    
    def _get_cross_area( self ):
        # fibers cross-sectional area -- circle 
        return pi * self.df ** 2 / 4.
    
    def cut( self, sx, lx, x ): #sx is the left fiber coordinate, lx is the horizontal length projection
        # cut condition
        if ( sx - lx / 2. <= x )and( x <= sx + lx / 2. ):
            return 1
        else:
            return 0  
    def cut_func( self, sx, lx, sec ):
        func = frompyfunc( self.cut, 3, 1 )
        return func( sx, lx, sec )
    
        
        

