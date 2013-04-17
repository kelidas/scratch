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

class D(HasTraits):
    x = Any

class A(HasTraits):
    b = Instance(B)

    dd = Instance(D)

    d = Button('test')
    def _d_fired(self):
        self.dd.x = B(str='xx')
    view = View('d')

class C(A):
    b = Property(Instance(B))
    def _get_b(self):
        return B(str='xxx')




a = A()
D().x.str
