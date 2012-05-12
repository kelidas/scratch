#-------------------------------------------------------------------------------
#
# Copyright (c) 2012
# IMB, RWTH Aachen University,
# ISM, Brno University of Technology
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in the Spirrid top directory "licence.txt" and may be
# redistributed only under the conditions described in the aforementioned
# license.
#
# Thanks for using Simvisage open source!
#
#-------------------------------------------------------------------------------

from traits.api import HasTraits, Array, Property, DelegatesTo, CTrait, \
    Instance, Int, Str, List, on_trait_change, Button, Trait, Dict, Enum
from traitsui.api import View, Item, DefaultOverride, EnumEditor
from itertools import combinations, chain
from matplotlib import rc
from socket import gethostname
from spirrid import SPIRRID
import numpy as np
import os.path
import pylab as p # import matplotlib with matlab interface
import types



class EnumExample(HasTraits):
    priority = Enum('Medium', 'Highest',
                              'High',
                              'Medium',
                              'Low',
                              'Lowest')

    view = View(Item(name='priority',
                      editor=EnumEditor(values={
                          'Highest' : '1:Highest',
                          'High'    : '2:High',
                          'Medium'  : '3:Medium',
                          'Low'     : '4:Low',
                          'Lowest'  : '5:Lowest', })))



test = EnumExample()
test.configure_traits()



