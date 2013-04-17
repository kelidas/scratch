'''
Created on 4.3.2012

@author: kelidas
'''
from traits.api import HasTraits, Property, cached_property, Event, \
    Array, Instance, Int, Directory, Range, on_trait_change, Bool, Trait, Constant, \
    Tuple, Interface, implements, Enum, Str
from traits.trait_types import DelegatesTo
from traitsui.api import Item, View, HGroup, RangeEditor
from numpy import loadtxt, min, array, arange, ones_like, cumsum, vstack, \
    hstack, sum, zeros_like, zeros, ones, where, unique, pi, invert, \
    prod
from os.path import join
from scipy.sparse import csr_matrix
import numpy.ma as ma
import numpy as np
import os
import re

class RFEM_Source(HasTraits):

    directory = Str(modified = True)

    nodes = Property(Array, depends_on = '+modified')
    def _get_nodes(self):
        data = np.loadtxt('nodes.txt', delimiter = ';', usecols = (1))
        return data

    lines = Property(Array, depends_on = '+modified')
    def _get_lines(self):
        data = np.loadtxt('nodes.txt', delimiter = ';', usecols = (1))
        return data

    mats = Property(Array, depends_on = '+modified')
    def _get_mats(self):
        data = np.loadtxt('nodes.txt', delimiter = ';', usecols = (1))
        return data

    areas = Property(Array, depends_on = '+modified')
    def _get_areas(self):
        data = np.loadtxt('nodes.txt', delimiter = ';', usecols = (1))
        return data

    opens = Property(Array, depends_on = '+modified')
    def _get_opens(self):
        data = np.loadtxt('nodes.txt', delimiter = ';', usecols = (1))
        return data

class ANSYS_Commands(HasTraits):

    rfem = Instance(RFEM_Source, modified = True)

    kps = Property(depends_on = '+modified')
    def _get_kps(self):
        cmd = ''
        for row_i, row in enumerate(self.rfem.nodes[3, 4, 5]):
            cmd += 'k, %i, %f, %f, %f' % (row_i, row[0], row[1], row[3])
        return cmd

    lines = Property(depends_on = '+modified')
    def _get_lines(self):
        cmd = ''
        for row_i, row in enumerate(self.rfem.nodes[3, 4, 5]):
            cmd += 'l, %i, %i' % (row_i, row[0], row[1], row[3])
        return cmd

    areas = Property(depends_on = '+modified')










