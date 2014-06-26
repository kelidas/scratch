# Copyright (c) 2007, Enthought, Inc.
# License: BSD Style.

"""
Implementation of an ImageEnumEditor demo plugin for the Traits UI demo program.

This demo shows each of the four styles of the ImageEnumEditor.
"""

# Imports:
from traits.api \
    import HasTraits, Str, Trait

from traitsui.api \
    import Item, Group, View, ImageEnumEditor, Handler

# This list of image names (with the standard suffix "_origin") is used to
# construct an image enumeration trait to demonstrate the ImageEnumEditor:

class Dummy ( HasTraits ):
    """ Dummy class for ImageEnumEditor
"""
    pass

class MyHandler(Handler):

    def object_name_from_list_changed(self, info):
        info.object.image_from_list = info.object.name_from_list


class ImageEnumEditorDemo ( HasTraits ):
    """ Defines the ImageEnumEditor demo class.
"""

    # Define a trait to view:
    
    image_list = [ 'eq', 'eq1' ]
    
    name_from_list = Trait(image_list)
    
    image_from_list = Trait( editor = ImageEnumEditor( values = image_list,
                                                       #prefix = '@icons:',
                                                       suffix = '',
                                                       cols = 2,
                                                       klass = Dummy ),
                             *image_list )

    # Items are used to define the demo display, one Item per editor style:
    img_group = Group(
        Item('name_from_list'),
        Item('_'),
        #Item( 'image_from_list', style = 'simple', label = 'Simple' ),
        #Item( '_' ),
        #Item( 'image_from_list', style = 'custom', label = 'Custom' ),
        #Item( '_' ),
        #Item( 'image_from_list', style = 'text', label = 'Text' ),
        #Item( '_' ),
        Item( 'image_from_list', style = 'readonly', label = 'ReadOnly' )
    )

    # Demo view:
    view = View(
        img_group,
        handler=MyHandler,
        title = 'ImageEnumEditor',
        buttons = [ 'OK' ],
        resizable = True
    )

# Create the demo:
demo = ImageEnumEditorDemo()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()

 
