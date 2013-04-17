'''
Created on 23.2.2012

@author: kelidas
'''
from threading import Thread
from time import sleep
from traits.api import *
from traitsui.api import View, Item, ButtonEditor
from pokusy.histogram.mpl_figure_editor import MPLFigureEditor
from matplotlib.figure import Figure
from traits.api import Instance, on_trait_change, \
                                 Event, Button

from traitsui.api import \
    View, Item, VGroup, ModelView, HSplit
from traitsui.menu import OKButton, MenuBar, Menu, Action
from pyface.action.group import Group
import numpy as np
from numpy.random import random

class TextDisplay(HasTraits):
    string = Array(input = True)

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor = 'white')
        figure.add_axes([0.15, 0.15, 0.75, 0.75])#[0.25, 0.25, 0.55, 0.55])#
        return figure

    data_changed = Event(True)

    @on_trait_change('+input')
    def _redraw(self):
        figure = self.figure
        axes = figure.axes[0]
        #axes.clear()
        axes.plot(self.string[0], self.string[1], 'ro')
        self.data_changed = True

    #view = View(Item('string', show_label = False, springy = True, style = 'custom'))

    view = View(Item('string'),
                Item('figure', editor = MPLFigureEditor(),
                     resizable = True, show_label = False))


class CaptureThread(Thread):
    def run(self):
        i = 0
        while not self.wants_abort:
            self.display.string = np.array([random(), random()])
            self.display._redraw()
            i += 1
            print i

class Camera(HasTraits):
    start_stop_capture = Button()
    display = Instance(TextDisplay)
    capture_thread = Instance(CaptureThread)

    view = View(Item('start_stop_capture', show_label = False))

    def _start_stop_capture_fired(self):
        if self.capture_thread and self.capture_thread.isAlive():
            self.capture_thread.wants_abort = True
        else:
            self.capture_thread = CaptureThread()
            self.capture_thread.wants_abort = False
            self.capture_thread.display = self.display
            self.capture_thread.start()

class MainWindow(HasTraits):
    display = Instance(TextDisplay, ())

    camera = Instance(Camera)

    def _camera_default(self):
        return Camera(display = self.display)

    view = View(Item('display', show_label = False),
                Item('camera', show_label = False),
                style = "custom",
                resizable = True,
                width = 0.5,
                height = 0.5,
                buttons = [OKButton])


if __name__ == '__main__':
    MainWindow().configure_traits()
