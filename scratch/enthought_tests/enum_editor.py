from traits.api import List, HasTraits, Str, Instance, Enum
from traitsui.api import EnumEditor, Group, View, Item

keys = ['a', 'b']
map = { 'a' : ['one', 'two'] , 'b' : ['three', 'four'] }

class DependentEnumExample( HasTraits ):
    first_enum = List( keys )
    second_enum = List

    first = Str( 'a' )
    second = Str


    traits_view = View( Group( Item( name = 'first', editor = EnumEditor( name = 'first_enum' ) ),
                             Item( name = 'second', editor = EnumEditor( name = 'second_enum' ) ) ) )
    def __init__( self ):
        self.second_enum = map[self.first]

    def _first_changed( self, new ):
        self.second_enum = map[self.first]


example = DependentEnumExample()
example.configure_traits()
