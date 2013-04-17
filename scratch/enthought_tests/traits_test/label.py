#! /usr/bin/env python
"""
Demo of how to specify ranges and label of a slider when create
"""

from traits.api import HasTraits, Button, Range, Int, Str
from traitsui.api import Item, View, Group, Label, HGroup, UReadonly
from traitsui.message import message

class GUISlider ( HasTraits ):

    mylow = Int( 5 )
    myhigh = Int( 10 )
    mylabel = Str( '123' )
    theslider = Range( value = 1, low = 'mylow', high = 'myhigh', desc = "How to set the range on the fly!" )

    settings_group = Group( 
         HGroup( 
            UReadonly( value = 'mylabel' ),
            Item( 'theslider', show_label = False )
        )
    )

    # The view includes one group per data type. These will be displayed
    # on separate tabbed panels:
    view = View( 
        settings_group,
        title = 'test',
        width = 450,
        buttons = ['OK', 'Cancel', 'Help' ],
        kind = 'modal',
    )

# Create the demo:
test_popup = GUISlider( mylow = 5, myhigh = 10, mylabel = 'The Label    ' )

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    test_popup.configure_traits()
