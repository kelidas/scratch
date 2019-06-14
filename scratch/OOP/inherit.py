from traits.api import HasTraits, HasStrictTraits, Array, Property, DelegatesTo, CTrait, \
    Instance, Int, Str, List, on_trait_change, Button, Trait, Dict, Enum
from traitsui.api import View, Item, DefaultOverride, EnumEditor

class M(HasStrictTraits):
    def p(self):
        print self.x + self.y

class A(M):
    x = Int(1)
    y = Int(4)

class B(M):
    x = Int(5)
    y = Int(4)

if __name__ == '__main__':
    a = A()
    a.p()
    b = B()
    b.p()
