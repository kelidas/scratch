'''
Created on May 12, 2011

@author: kelidas
'''

from traits.api import HasTraits, Property, cached_property, Event, \
    Array, Instance, Int, Directory, Range, on_trait_change, Bool, Trait, Constant, \
    Tuple, Interface, implements, Enum, File, Str
from traits.trait_types import DelegatesTo
from traitsui.api import Item, View, HGroup, RangeEditor, Group, HSplit, VGroup, FileEditor
from matplotlib.figure import Figure
from mpl_figure_editor import MPLFigureEditor
from numpy import array, vstack, linspace, unique
from numpy import loadtxt, min, array, arange, ones_like, cumsum, vstack, \
    hstack, sum, zeros_like, zeros, ones, where, unique, pi, invert, \
    prod
from os.path import join
from os.path import split as os_path_split
import matplotlib.pyplot as plt
import re

class OOData( HasTraits ):
    '''
    Prepare data from OOFFEM output file
    '''

    out_file = File( 'data.out', filter = [ 'oofem out (*.out)|*.out',
                                            'text files (*.txt)|*.txt',
                                             'all files (*.*)|*.*' ],
                                              source_modified = True )

    node = Int( 330, auto_set = False, enter_set = True, conf_modified = True )

    nodes = Property( Str, depends_on = '+source_modified' )
    def _get_nodes( self ):
        return unique(self.reaction_data[:, 0])


    reaction_data = Property(Array, depends_on='+source_modified')
    @cached_property
    def _get_reaction_data(self):
        input_file = open( self.out_file, 'r' )
        data = array( [] ).reshape( 0, 3 )
        while 1:
            line = self._locate_line( input_file, r'^\s+Node\s+\d+\s+iDof\s+\d+\s+reaction\s+' )
            if not line: break
            splt = line.split()
            data = vstack( [data, array( [float( splt[1] ), float( splt[3] ), float( splt[5] )] ) ] )
        input_file.close()
        return data

    def _locate_line( self, file_object, info_pattern ):
        '''
        Reads lines from file_object until it reaches a line which matches the RegEx pattern
        given in 'info_pattern'. Used to position file cursor to the correct place for 
        reading in arbitraty order.
        '''
        info_matcher = re.compile( info_pattern )
        info_line = ' '
        while not info_matcher.search( info_line ) and info_line != '':
            info_line = file_object.readline()
        return info_line

    traits_view = View( 
                       Item( 'out_file', style = 'simple', springy = True ),
                       Item( 'out_file', style = 'custom', springy = True, show_label = False ),
                       '_',
                       Item( 'node', springy = True ),
                       Item( 'nodes', style = 'readonly' )
                )



class OOReader( HasTraits ):
    '''
    OOFFEM output data reader -- display ld-diagrams
    '''

    data = Instance( OOData )

    figure = Instance( Figure )

    def _figure_default( self ):
        figure = Figure()
        figure.add_axes( [0.15, 0.15, 0.75, 0.75] )
        return figure

    data_changed = Event( True )
    @on_trait_change( 'data.+conf_modified, data.+source_modified' )
    def _redraw( self ):
        figure = self.figure
        axes = figure.axes[0]
        axes.clear()
        mask = self.data.reaction_data[:, 0] == self.data.node
        axes.plot(hstack([0, self.data.reaction_data[mask][:, 2]]), 'b-x', linewidth=2)
        axes.set_title( os_path_split( self.data.out_file )[-1] )
        axes.set_xlabel( 'step', fontsize = 16 )
        axes.set_ylabel( 'force', fontsize = 16 )#, fontsize = 16
        plt.setp( axes.get_xticklabels(), position = ( 0, -.01 ) )
        self.data_changed = True

    traits_view = View( 
                  HSplit( 
                        VGroup( Item( 'data@', show_label = False, springy = True ),
                       id = 'reader.settings',
                       label = 'settings',
                       dock = 'tab',
                       ),
                       Group( 
                                        Item( 'figure', editor = MPLFigureEditor(),
                                               show_label = False, resizable = True ),
                                        label = 'Plot sheet',
                                        id = 'reader.figure_window',
                                        dock = 'tab',
                                        ),
                                id = 'reader.hsplit',
                                 ),
                resizable = True,
                id = 'reader.main.view',
                )






if __name__ == '__main__':
    data = OOData()
    reader = OOReader( data = data )
    reader.configure_traits()











