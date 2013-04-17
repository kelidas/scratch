from traits.api import HasTraits, HasStrictTraits, Float, Property, cached_property, \
                                Instance, List, on_trait_change, Int, Tuple, Bool, Interface, \
                                DelegatesTo, Event, Enum, implements, Button, File, CFloat, Str

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
from numpy import arccos, matrix, sum, arange, memmap

import matplotlib.pylab as plt


class Customer( Interface ):
    name = Str()
    address = Str()
    email = Str()
    def print_( self ):
        pass
    
    
class company( HasTraits ):
    implements( Customer )
    ico = Int()
    dic = Int()
    account = Int()
    def print_( self ):
        print 'name = ', self.name
        print 'ico = ', self.ico
        print 'dic = ', self.dic
        print 'address = ', self.address
        print 'email = ', self.email
        print 'account = ', self.account

class individual( HasTraits ):
    implements( Customer )
    def print_( self ):
        print 'name = ', self.name
        print 'addres = ', self.address
        print 'email = ', self.email


c1 = company()
c2 = individual()
c1.set( name='rfem', address='brno', email='c@c.cz', ico=12546232, dic=5641645, account=651654 )
c2.set( name='vasek', address='vm', email='vasek@c.cz' )
print c1
c1.print_()
c2.print_()
c1.configure_traits()
c2.configure_traits()
