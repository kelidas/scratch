#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.

from traits.api import HasTraits, Str, Trait

from traitsui.api import View, VGroup, Item, Handler

from traitsui.api import ImageEditor

from pyface.image_resource import ImageResource

class MyHandler(Handler):

    def object_equations_changed(self, info):
        info.object.equation = info.object.equations[0]
        
        
class Employee ( HasTraits ):

    # Define the traits:
    equation  = Str
    equations = Trait('eq1.png', ['eq.png', 'eq1.png'])

    # Define the view:
    view = View(
        Item('equations'),
        Item( 'equation',
                      show_label = True,
                      editor = ImageEditor(
                          image = ImageResource('eq1.png') ) ),           
        handler = MyHandler,
    )

# Create the demo:
popup = Employee( )

# Run the demo (if invoked form the command line):
if __name__ == '__main__':
    popup.configure_traits()