from traits.api import HasTraits, HasStrictTraits, Array, Property, DelegatesTo, CTrait, \
    Instance, Int, Str, List, on_trait_change, Button, Trait, Dict, Enum, Interface, implements
from traitsui.api import View, Item, DefaultOverride, EnumEditor

class IA(Interface):
    def test(self):
        ''''''

class A(HasStrictTraits):
    implements(IA)
    def test(self):
        print 'A'

class B(HasTraits):
    implements(IA)
    def test(self):
        print 'B'

class C(HasTraits):
    a = Instance(A)
    def test(self):
        self.a.test()

class D(HasTraits):
    a = Instance(IA)
    def test(self):
        self.a.test()

if __name__ == '__main__':
    b = B()
    b.test()
    a = A()
    a.test()

    d = D(a=A())
    d.test()

    d = D(a=B())
    d.test()

    c = C(a=A())
    c.test()

    c = C(a=B())
    c.test()

