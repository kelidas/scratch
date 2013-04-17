#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.#-- Imports --------------------------------------------------------------------

from numpy.random \
    import random

from traits.api \
    import HasTraits, Array, Int, Property

from traitsui.api \
    import View, Item

from traitsui.ui_editors.array_view_editor \
    import ArrayViewEditor

#-- ShowArray demo class -------------------------------------------------------

class ShowArray ( HasTraits ):

    row = Int( 5, enter_set = True, auto_set = False )

    data = Property( Array, depends_on = 'row' )
    def _get_data( self ):
        return random( ( self.row, 3 ) )

    view = View( 'row',
        Item( 
             'data',
              show_label = False,
              editor = ArrayViewEditor( titles = [ 'x', 'y', 'z' ],
                                            format = '%.4f',
                                            font = 'Arial 8' )
        ),
        title = 'Array Viewer',
        width = 0.3,
        height = 0.8,
        resizable = True
    )

#-- Run the demo ---------------------------------------------------------------

# Create the demo:
demo = ShowArray()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
