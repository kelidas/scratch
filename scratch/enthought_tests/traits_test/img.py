

from traits.api import HasTraits, Button, Range, Int, Str, Directory, \
                             cached_property, List, Property, Tuple
from traitsui.api import Item, View, Group, Label, HGroup, UReadonly, Handler
import os
import Image
from os.path import join
import pyexiv2


class TitleHandler( Handler ):
    """ Change the title on the UI.
    """

    def object_yarn_type_changed( self, info ):
        """ Called whenever the "yarn" attribute changes on the handled
        object.
        """
        info.ui.title = 'Image Editor'


class ImgEditor( HasTraits ):
    directory = Directory()

    files = Property( List, depends_on = 'directory' )
    @cached_property
    def _get_files( self ):
        return [f for f in os.listdir( self.directory ) if f.lower().endswith( '.jpg' )]

    dim = Tuple( ( 2, 3 ), tooltip = 'tip' )

    run = Button()
    def _run_fired( self ):
        for f in self.files:
            im = Image.open( join( self.directory, f ), 'r' )
            w, h = im.size
            print w, h
            new_w, new_h = self.dim
            pom = float( h ) / float( w )
            dir_name = 'resized'
            try:
                os.mkdir( join( self.directory, dir_name ) )
            except:
                pass
            if pom < 1.0:
                im_res = im.resize( ( int( new_w ), int( new_w * pom ) ) )
                im_res.save( join( self.directory, dir_name, f ), 'JPEG' )
            else:
                im_res = im.resize( ( int( new_h / pom ), int( new_h ) ) )
                im_res.save( join( self.directory, dir_name, f ), 'JPEG' )

            # copy EXIF data
            source_image = pyexiv2.Image( join( self.directory, f ) )
            source_image.readMetadata()
            dest_image = pyexiv2.Image( join( self.directory, dir_name, f ) )
            dest_image.readMetadata()
            source_image.copyMetadataTo( dest_image )

            # set EXIF image size info to resized size
            dest_image["Exif.Photo.PixelXDimension"] = im.size[0]
            dest_image["Exif.Photo.PixelYDimension"] = im .size[1]
            dest_image.writeMetadata()


    traits_view = View( Item( 'directory', show_label = True, springy = True ),
                        Item( 'dim', label = 'w x h' ),
                        Item( 'run', show_label = False ),
                        #resizable = True,
                        #scrollable = True,
                        title = 'Image Editor',
                        #handler = TitleHandler(),
                        #width = .8,
                        #height = .5
                                 )



# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    ed = ImgEditor()
    ed.configure_traits()
