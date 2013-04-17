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

# @todo: very short spec
def probability_cut_nooverlaps( lc, lf, delta ):
    '''
        Probability that we cut fiber of nooverlapped fibers
    '''
    #type I and III
    if ( lf <= lc / 2. - delta ) and ( lf <= lc / 2. + delta ):
        #print "Varianta I or III ",
        return lc / lf * ( ln( lc / ( lc - lf ) ) ) - 1
    #type II
    if ( lf < lc / 2. + delta ) and ( lf > lc / 2. - delta ):
        #print "Varianta II ",
        return 1 / 2. / lf * ( ( lc + 2. * delta ) * ln( 2. / ( lc + 2. * delta ) ) - ( ln( lc - lf ) + 1 ) * ( lc - 2. * delta ) + 2. * lc * ln( lc ) )
    #type IV
    if ( lf >= lc / 2. + delta ) and ( lf >= lc / 2. - delta ):
        #print "Varianta IV ",
        return  1 + 1 / lf * ( -lc + ( lc / 2. - delta ) * ln( ( lc + 2 * delta ) / ( lc - 2 * delta ) ) + lc * ln( 2 * lc / ( lc + 2 * delta ) ) )


