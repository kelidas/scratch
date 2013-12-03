from traits.api import \
    HasTraits, Float, Property, cached_property, Int, Array, Bool, \
    Instance, DelegatesTo, Tuple, Button, List, Str, Directory, Enum, on_trait_change

from traitsui.api import View, Item, HGroup, EnumEditor, Group, UItem, RangeEditor, \
                    CheckListEditor, HSplit

from mpl_figure_editor import MPLFigureEditor
import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os
import re
from matplotlib.figure import Figure


import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock


ROOTDIR = '/media/data/Documents/postdoc/2013/Smidova/seed=run/'
sampling_lst = ['MC', 'LHS']
norm_lst = ['Pearson', 'Spearman', 'AE']
method_lst = ['RandMixSwitch', 'SA', 'RandomSwitch']
function_lst = ['Minima', 'Soucet_cosinu', 'Soucet_exp', 'Soucet_kvadratu',
                'Soucet_NV', 'Soucin']


class DirSelector(HasTraits):

    database_dir = Directory(ROOTDIR)

    sampling = List(sampling_lst, editor=CheckListEditor(
                           values=sampling_lst,
                           cols=1))

    norm = List(norm_lst, editor=CheckListEditor(
                           values=norm_lst,
                           cols=1))

    method = List(method_lst, editor=CheckListEditor(
                           values=method_lst,
                           cols=1))

    function = List(['Minima'], editor=CheckListEditor(
                           values=function_lst,
                           cols=1))

    traits_view = View(
                       'database_dir',
                       Group(Item('sampling@'), show_border=True),
                       Group(Item('norm@'), show_border=True),
                       Group(Item('method@'), show_border=True),
                       Group(Item('function@'), show_border=True)
                       )



class Plot(HasTraits):

    name = 'plot'

    selector = Instance(DirSelector)

    # data = Instance(RecursionData)

    plot_list = List

    figure = Instance(Figure)

    # plot_selector = Instance(PlotSelector)

    clear_on = Bool(True)

    draw = Button()

    delete_last_one = Button('Delete last line in the plot')
    def _delete_last_one_fired(self):
        axes0 = self.figure.axes[0]
        axes1 = self.figure.axes[1]
        if len(axes0.lines) != 0:
            axes0.lines.pop(-1)
            self.figure.canvas.draw()
        else:
            print 'There are no lines in the figure!'
        if len(axes1.lines) != 0:
            axes1.lines.pop(-1)
            self.figure.canvas.draw()
        else:
            print 'There are no lines in the figure!'

    def _draw_fired(self):
        axes0 = self.figure.axes[0]
        axes1 = self.figure.axes[1]
        if self.clear_on:
            axes0.clear()
            axes1.clear()
        path = []
        for s in self.selector.sampling:
            for n in self.selector.norm:
                for m in self.selector.method:
                    path.append(os.path.join(ROOTDIR, s, n, m, 'Results'))
        print path
        for p in path:
            result_files = os.listdir(path[0])
            for f in self.selector.function:
                function_files = []
                for rf in result_files:
                    r = re.compile(f)
                    if r.search(rf):
                        function_files.append(rf)
                print function_files
                x0 = []
                y0 = []
                y1 = []
                for ff in function_files:
                    data = np.loadtxt(os.path.join(p, ff), skiprows=1)
                    x0.append(data[:, 1].mean())
                    y0.append(data[:, 2].mean())
                    y1.append(data[:, 3].mean())
                axes0.semilogx(x0, y0, marker='x', linewidth=2)
                axes1.semilogx(x0, y1, marker='x', linewidth=2,
                              label=p.replace(ROOTDIR, '').replace('/Results', ''))
                axes1.legend(loc='best')

        # wx.CallAfter(self.figure.canvas.draw)
        self.figure.canvas.draw()

    traits_view = View(
                       'clear_on',
                       HGroup(
                              Item('draw', show_label=False, springy=True),
                              Item('delete_last_one', show_label=False, springy=True),
                       ),
                       id='plot.main'
                       )





class ControlPanel(HasTraits):

#     load_info = String()
#
#     data = Instance(RecursionData, ())
    selector = Instance(DirSelector, ())
#     python_shell = Instance(PythonShell, ())
#
#     plot_selector = Instance(PlotSelector)
#     def _plot_selector_default(self):
#         return PlotSelector(data=self.data)
#
#     @on_trait_change('data')
#     def _plot_selector_deflt(self):
#         return PlotSelector(data=self.data)
#
    plot = Instance(Plot)
#     plot = EitherType(names=['wp plot',
#                              'pdf plot',
#                              'cdf_plot',
#                              'diff_plot',
#                              'tangent parameter plot',
#                              'base',
#                              ],
#                       klasses=[WPPlot,
#                                PDFPlot,
#                                CDFPlot,
#                                DiffPlot,
#                                TangentParameterPlot,
#                                BasePlot,
#                                ])
#
    def _plot_default(self):
        return Plot(figure=self.figure, selector=self.selector)
#
    @on_trait_change('plot')
    def _plot_deflt(self):
        self.plot.data = self.data
        self.plot.figure = self.figure
        self.plot.plot_selector = self.plot_selector
#
#     load_thread = Instance(LoadThread)
#
#     start_stop_loading = Button('Start/Stop loading')
#
#     def _start_stop_loading_fired(self):
#         if self.load_thread and self.load_thread.isAlive():
#             self.load_thread.wants_abort = True
#         else:
#             self.load_thread = LoadThread()
#             self.load_thread.load_info_display = self._add_line
#             self.load_thread.data = self.data
#             self.load_thread.selector = self.selector
#             self.load_thread.start()
#
#     def _add_line(self, string):
#         """ Adds a line to the info box display.
#         """
#         self.load_info = (string + '\n' + self.load_info)  # [0:1000]

    traits_view = View(
                       Group(
                             Item('selector@', show_label=False, enabled_when='load_thread.wants_abort'),
                             Item('plot', style='custom', show_label=False),
#                              Item('start_stop_loading', show_label=False),
#                              Group(
#                              Item('load_info', show_label=False, style='custom'),
#                              label='Load info', show_border=True
#                              ),
#                              label='load control',
                             dock='tab', id='control_panel.load_control'),
#                        Group(
#                              Item('plot_selector', show_label=False, style='custom'),
#                              label='plot selector',
#                              dock='tab',
#                              id='control_panel.plot_selector',
#                        ),
#                         Group(
#                               Item('plot', style='custom', show_label=False),
#                               label='plot control',
#                               dock='tab',
#                               id='control_panel.plot',
#                         ),
#                        Group(
#                              Item('python_shell@', show_label=False),
#                              label='shell',
#                              dock='tab',
#                              id='control_panel.shell',
#                              ),
                       id='control_panel.main'
                       )


class MainWindow(HasTraits):

    figure = Instance(Figure)

    panel = Instance(ControlPanel)

    def _panel_default(self):
        return ControlPanel(figure=self.figure)

    def _figure_default(self):
        figure = Figure(tight_layout=True)
        figure.add_subplot(1, 2, 1)
        figure.add_subplot(1, 2, 2)
        # figure.add_axes([0.2, 0.04, 0.7, 0.8])
        return figure

    view = View(HSplit(
                       Item('panel@', show_label=False,
                            width=0.4, id='main_window.panel'),
                       Item('figure', editor=MPLFigureEditor(), show_label=False,
                            width=0.6, dock='tab', id='main_window.figure'),
                       id='main_window.hsplit',
                       ),
                title='Recursion Analyzer',
                id='main_window.view',
                resizable=True,
                height=0.7,
                width=0.75,
                # buttons=[OKButton],
                )








if __name__ == '__main__':
    app = MainWindow()
    app.configure_traits()
    # d = DirSelector()
    # d.configure_traits()











