'''
Created on Mar 2, 2010

@author: kelidas
'''

#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.
#-- Imports --------------------------------------------------------------------

from traits.api \
    import HasTraits, Str, File, Directory
    
from traitsui.api \
    import View, Item, FileEditor, DirectoryEditor, HistoryEditor

#-- HistoryDemo Class ----------------------------------------------------------

class HistoryDemo ( HasTraits ):
    
    name = Str
    file = File
    directory = Directory
    
    view = View( 
        Item( 'name',
              id='name',
              editor=HistoryEditor( entries=5 )
        ),
        Item( 'file',
              id='file1',
              editor=FileEditor( entries=10 )
        ),
        Item( 'file',
              id='file2',
              editor=FileEditor( entries=10,
                                   filter=[ 'Python files (*.py)|*.py' ] )
        ),
        Item( 'directory',
              id='directory',
              editor=DirectoryEditor( entries=10 )
        ),
        title='History Editor Demo',
        id='enthought.test.history_demo.HistoryDemo',
        width=0.33,
        resizable=True
    )

# Create the demo:    
demo = HistoryDemo()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()
