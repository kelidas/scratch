'''
Created on Mar 1, 2010

@author: kelidas
'''

from traits.api import HasTraits, \
                                 Int, Enum, File, Bool


from traitsui.api import View, Item, HSplit, VGroup

from traitsui.menu import OKButton

from numpy import loadtxt

class Histogram (HasTraits):

    file = File(value='CSN-Weibull-200ksim.txt', filter=[ 'Python files (*.txt)|*.txt' ], exists=True, modified=True)
    bins = Int(50, auto_set=False, enter_set=True, modified=True)
    #range = ( 0, 1000 )
    normed = Bool(True, modified=True, desc='popisek')
    #weights = 
    cumulative = Bool(False, modified=True)
    histtype = Enum('bar' , 'barstacked' , 'step' , 'stepfilled' , modified=True)
    align = Enum('left', 'mid', 'right', modified=True)
    orientation = Enum('vertical' , 'horizontal', modified=True)
    #rwidth = 'None'
    log = Bool(False, modified=True)

    param_names = ['file', 'bins', 'range', 'normed', 'weights', 'cumulative', 'histtype', 'align', \
                    'orientation', 'rwidth', 'log']

    #def __init__( self, **kw ):
    #    super( Histogram, self ).__init__( **kw )

    def get_data(self):
        try:
            return loadtxt(self.file)
        except:
            print 'chyba'
            return False

    traits_view = View(HSplit(VGroup(
                                              Item('file', id='file1'), #,editor=FileEditor( entries=10,
                                                    #auto_set=True, filter=[ 'Python files (*.txt)|*.txt' ] ) ),
                                              Item('bins', label='bins'),
                                              #Item( 'range', label='range' ),
                                              Item('normed', label='normed'),
                                              #Item( 'weights', label='weight' ),
                                              Item('cumulative', label='cumulative'),
                                              Item('histtype', label='histogram type'),
                                              Item('align', label='align'),
                                              Item('orientation', label='orientation'),
                                              #Item('rwidth', label='rwidth'),
                                              Item('log', label='log scale axis'),
                                              label='Histogram parameters',
                                              id='histog.params'
                                              ),
                                        id='histog.vgroup'
                                        ),
                        resizable=True,
                        #height=0.8,
                        #width=.5,
                        buttons=[OKButton],
                        id='histog.view'
                        )



if __name__ == '__main__':
    histogram = Histogram()
    histogram.configure_traits()
