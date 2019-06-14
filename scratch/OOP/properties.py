from traits.api import HasTraits, HasStrictTraits, Array, Property, DelegatesTo, CTrait, \
    Instance, Int, Str, List, on_trait_change, Button, Trait, Dict, Enum
from traitsui.api import View, Item, DefaultOverride, EnumEditor

class A(HasStrictTraits):
    n = Int
    d = Property(Int)
    def _get_d(self):
        print 'jsem tu', self.n
        return self.n

class B(HasStrictTraits):
    nb = Int

class C(B):
    nc = Int

class D(C):
    nd = Int

if __name__ == '__main__':
    A(n=2).d
    A(n=10).d
