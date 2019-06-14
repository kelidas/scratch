from traits.api import HasTraits, HasStrictTraits, Array, Property, DelegatesTo, CTrait, \
    Instance, Int, Str, List, on_trait_change, Button, Trait, Dict, Enum
from traitsui.api import View, Item, DefaultOverride, EnumEditor

class A(HasTraits):
    n = Int

class B(HasStrictTraits):
    n = Int

if __name__ == '__main__':
    a = A(n=5, m=6)
    b = B(n=5, m=6)
