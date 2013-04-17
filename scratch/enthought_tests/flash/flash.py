#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.# Imports:
from traitsui.wx.extra.windows.flash_editor \
    import FlashEditor
    
from traits.api \
    import Enum, HasTraits
    
from traitsui.api \
    import View, HGroup, Item
    
# The demo class:
class FlashDemo ( HasTraits ):
    
    # The Flash file to display:
    flash = Enum( 'example.swf' )
                   
    # The view to display:
    view = View( 
        HGroup( 
            Item( 'flash', label='Pick a game to play' )
        ),
        '_',
        Item( 'flash',
              show_label=False,
              editor=FlashEditor()
        )
    )
    
# Create the demo:    
demo = FlashDemo()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
