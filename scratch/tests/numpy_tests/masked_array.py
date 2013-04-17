'''
Created on Nov 21, 2010

@author: kelidas
'''
from mayavi import mlab
from mayavi.stats.spirrid.ui.api import MlabSceneModel, SceneEditor
from mayavi.stats.spirrid.ui.mayavi_scene import MayaviScene
from mayavi.tools.mlab_scene_model import MlabSceneModel
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, File, Int, Directory, Button, Range, Enum, \
     on_trait_change, Either, Dict
from traitsui.api import Item, View, Group, Handler, HSplit, VSplit, \
    HGroup, HSplit, VGroup, Tabbed, Label, Controller, ModelView
from traitsui.api import View, Item, FileEditor, DirectoryEditor, \
    HistoryEditor, RangeEditor
from traitsui.menu import OKButton, CancelButton, Action, Menu, \
    MenuBar
from enthought.tvtk.pyface.scene_editor import SceneEditor 
from matplotlib.figure import Figure
from numpy import sin, cos, linspace, pi, mean, sum
from numpy.random import random


from mayavi import mlab
from numpy.random import random
from numpy import arange, array
import numpy.ma as ma








arr1 = array( [[-1, 1], [2, 3]] )
marr1 = ma.masked_array( arr1, mask=[[1, 0], [0, 0]] )
print 'array 1', marr1

arr2 = array( [[6, 7], [9, -5]] )
marr2 = ma.masked_array( arr2, mask=[[0, 0], [0, 1]] )
print 'array2 ', marr2

print 'sum arrays', marr1 + marr2

mask = [[1, 0], [0, 0]]
a = ma.masked_array( [[5, 3], [3, 9]], mask=mask )
print 'array a', a
print sum( a )

print a.mask 


 




