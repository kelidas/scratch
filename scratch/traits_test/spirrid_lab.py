'''
Created on Dec 16, 2011

@author: kelidas
'''


from enthought.traits.api import HasTraits, Array, Property, DelegatesTo, \
    Instance, Int, Str, List, on_trait_change, Button, Float
from enthought.traits.ui.api import View, Item
from itertools import combinations, chain
from matplotlib import rc
from socket import gethostname
from stats.spirrid import SPIRRID
import numpy as np
import os.path
import pylab as p  # import matplotlib with matlab interface
import types


class SPIRRIDLAB(HasTraits):

    sampling_structure_btn = Button(label='compare sampling structure')

    @on_trait_change('sampling_structure_btn')
    def sampling_structure(self, **kw):
        '''Plot the response into the file in the fig subdirectory.
        '''
        p.plot([0, 5], [0, 5])
        p.show()

    traits_view = View(Item('sampling_structure_btn', show_label=False),
                       width=0.2,
                       height=0.2,
                       buttons=['OK', 'Cancel'])

if __name__ == '__main__':

    slab = SPIRRIDLAB()

    slab.configure_traits(kind='live')
