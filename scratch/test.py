from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

from etsproxy.traits.api import \
    HasTraits, Int, Array, Str, implements, Range, Property, cached_property, \
     Float, Instance, Any, Interface, Event, on_trait_change, Button, Bool, Callable
from etsproxy.traits.ui.api import \
    View, Item, Group, VGroup, HGroup, HSplit, VSplit, Tabbed
from math import pi, e
from mathkit.mfn.mfn_line.mfn_line import \
    MFnLineArray
from numpy import \
    sign, linspace, array, cos, sqrt, argmax, hstack, max, zeros_like, argwhere, loadtxt
from spirrid.i_rf import \
    IRF
from spirrid.rf import RF
from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor



class B(HasTraits):
    str = Str('B')

B().configure_traits()
