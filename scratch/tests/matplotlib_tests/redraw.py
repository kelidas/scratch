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

from traits.api import HasTraits, Instance, Button, Any
from traitsui.api import View, Item
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt


class Test(HasTraits):
    figure = Instance(Figure)

    def _figure_default(self):
        import matplotlib.pyplot as plt
        figure = plt.figure()
        figure.add_subplot(111)
        return figure

    axes = Any

    plot_data = Button
    def _plot_data_fired(self):
        figure = self.figure
        self.axes = figure.axes[0]
        self.axes.clear()
        self.axes.plot([0, 1], [0, 1])
        plt.show()

    redraw_data = Button
    def _redraw_data_fired(self):
        self.axes.plot([0, 2], [0, 1])
        self.figure.canvas.draw()

    view = View('plot_data', 'redraw_data')


if __name__ == '__main__':
    test = Test()
    test.configure_traits()
