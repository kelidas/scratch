'''
Created on Mar 1, 2010

@author: kelidas
'''
from traits.api import Instance, on_trait_change, \
                                 Event, Button

from traitsui.api import \
    View, Item, VGroup, ModelView, HSplit
from traitsui.menu import OKButton, MenuBar, Menu, Action

from pyface.image_resource import ImageResource
from pyface.action.group import Group

from mpl_figure_editor import MPLFigureEditor
from matplotlib.figure import Figure

from pyface.file_dialog import FileDialog

from histogram import Histogram
import pickle


class HistogramView( ModelView ):
    '''
    View for response functions
    '''

    model = Instance( Histogram )
    kb = Button( label = 'save as eps' )

    def _kb_fired ( self ):
            return self._save_figure()

    OpenAction = Action( 
                name = '&Open...',
                accelerator = "CTRL+O",
                action = '_on_open',
                image = ImageResource( "icons/open16.png" )
                )
    SaveAction = Action( 
                name = '&Save as...',
                accelerator = "CTRL+S",
                action = '_on_save_as',
                image = ImageResource( "icons/save16.png" )
                )
    CloseAction = Action( name = '&Close', accelerator = "CTRL+C", action = '_on_close', image = ImageResource( "icons/close16.png" ) )

    def _on_open( self, info ):
        """ Menu action to load a script from file.  """
        print '_on_open(%r)' % info
        file_dialog = FileDialog( action = 'open',
        #    default_directory=info.object.file_directory,
            wildcard = 'All files (*.*)|*.*' )
        print 'file_dialog'
        file_dialog.open()
        print 'open'
        #if file_dialog.path != '':
        #    info.object.load_code_from_file( file_dialog.path )
        try:
            print file_dialog.path
            pkl_file = open( file_dialog.path, 'rb' )
            self.model = pickle.load( pkl_file )
            pkl_file.close()
        except IOError:
            print 'Wrong or no input file!'
        return

    def _on_save_as( self, info ):
        """ Menu action to save script to file of different name """
        file_dialog = FileDialog( action = 'save as',
        #                         #default_path=info.object.file_path,
                                 wildcard = 'All files (*.*)|*.*' )
        file_dialog.open()
        try:
            output = open( file_dialog.path, 'wb' )
            pickle.dump( self.model , output )
            output.close()
        except IOError:
            print 'Wrong or no output file!'
        #if file_dialog.path != '':
        #    info.object.save_code_to_file( file_dialog.path )
        #    msg = 'Saving script at ', file_dialog.path
        #    logger.debug( msg )
        return

    figure = Instance( Figure )
    def _figure_default( self ):
        figure = Figure( facecolor = 'white' )
        figure.add_axes( [0.25, 0.25, 0.55, 0.55] )#[0.15, 0.15, 0.75, 0.75]
        return figure

    data_changed = Event( True )

    @on_trait_change( 'model.+modified' )
    def _redraw( self ):
        figure = self.figure
        axes = figure.axes[0]
        axes.clear()
        if  str( self.model.get_data() ) == 'False':
            axes.set_title( 'File error' , \
                            size = 'x-large', \
                            weight = 'bold', position = ( .5, 1.03 ) )
        else:
            data = self.model.get_data()
            #print self.model.get_data()
            axes.hist( data, self.model.bins, normed = self.model.normed , \
                        cumulative = self.model.cumulative , histtype = self.model.histtype, \
                        align = self.model.align, orientation = self.model.orientation, \
                        log = self.model.log, facecolor = 'blue', alpha = .3 )
            axes.set_xlabel( 'g(X) = R - E', weight = 'semibold' )
            axes.set_ylabel( 'Probability' , weight = 'semibold' )
            axes.set_title( 'Histogram ' + r'$g(X)$' , \
                            size = 'x-large', \
                            weight = 'bold', position = ( .5, 1.03 ) )
            #axes.axis( [0, 4000, 0, 0.0012] )
            axes.grid( True )
            axes.set_axis_bgcolor( color = 'white' )
            axes.grid( color = 'gray', linestyle = '--', linewidth = 0.2, alpha = 0.75 )
        self.data_changed = True

    def _save_figure( self ):
        fname = open( 'image.eps', 'w' )
        self.figure.savefig( fname, format = 'eps' )
        fname.close()
        return True

    traits_view = View( 
                       HSplit( 
                               VGroup( Item( 'model@', show_label = False, resizable = True, width = .2 ),
                                       'kb',
                                       id = 'histog.model',
                                       dock = 'tab',
                                       label = 'Histogram parameters',
                                       ),
                                VGroup( 
                                        Item( 'figure', editor = MPLFigureEditor(),
                                        resizable = True, show_label = False ),
                                        label = 'Plot sheet',
                                        id = 'histog.figure_window',
                                        dock = 'tab',
                                        ),
                                 ),
                        title = 'Histogram',
                        id = 'histog.viewmodel',
                        dock = 'tab',
                        resizable = True,
                        #width=.2, #height=.8,
                        menubar = MenuBar( Menu( Group( OpenAction, SaveAction ), Group( CloseAction ), name = 'File' ) ),
                        buttons = [OKButton] )

if __name__ == '__main__':
    histog = HistogramView( model = Histogram() )
    histog.configure_traits()

