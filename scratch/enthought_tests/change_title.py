'''
Created on May 18, 2011

@author: kelidas
'''

from traits.api import HasTraits, Str
from traitsui.api import Handler, Item, View


class TitleHandler( Handler ):
    """ Change the title on the UI.
    """

    def object_title_text_changed( self, info ):
        """ Called whenever the "title_text" attribute changes on the handled
        object.
        """
        info.ui.title = info.object.title_text


class TitleChanger( HasTraits ):
    """ Demonstrate the changing of the title.
    """

    title_text = Str( u"The default", auto_set = True )

    traits_view = View( 
        Item( 'title_text' ),
        title = u"The default",
        handler = TitleHandler(),
    )


tc = TitleChanger()
tc.configure_traits()
