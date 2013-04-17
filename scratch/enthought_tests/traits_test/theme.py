'''
Created on 11.6.2011

@author: Kelidas
'''
# themed.py -- Example of a Traits UI with themes
from traits.api import HasTraits, Str, Range, Float, Enum
from traitsui.api import View, Group, Item, Label
from traitsui.wx.themed_text_editor import ThemedTextEditor

class Test ( HasTraits ):

    name = Str
    age = Range( 1, 100 )
    weight = Float
    gender = Enum( 'Male', 'Female' )

    view = View( 
        Group( 
            Group( 
                Label( 'A Themed Label', '@GF6' ),
                Item( 'name' ),
                Item( 'age' ),
                Item( 'weight', editor = ThemedTextEditor() ),
                Item( 'gender' ),
                group_theme = '@GD0'
            ),
            group_theme = '@G',
            item_theme = '@B0B',
            label_theme = '@BEA'
        ),
        title = 'Themed Traits UI',
    )

Test().configure_traits()
