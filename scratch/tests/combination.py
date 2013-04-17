#import itertools
from itertools import combinations, chain


print list(combinations('ABCD', 2))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


X1 = 'a'
X2 = 'b'
X3 = 'c'
print list(powerset('ABCD'))
a=list(powerset([X1,X2,X3]))
print a
print a[1]


from traits.api import \
    HasTraits, Instance, List, Property, Array, Int, Any, cached_property, Dict, \
    Event, on_trait_change, Bool, Float, WeakRef, Str
class A( HasTraits ):
    a = Float(1.0)
    b= Float(2.0)
    aa = Property()
    def _get_aa(self):
        return self.a*self.a
    bb = Property()
    def _get_bb(self):
        return self.b*self.a

c=A()
dict_a={ 'a' : 20.}
dict_b={ 'a' : 20., 'b':50.}
list_a = ('c.set(a=3.)',)
list_b = ('c.set(a=3.)', 'c.set(b=5.)')
c.set(*list_a, **dict_a)
print c.a
print c.aa
print c.bb














