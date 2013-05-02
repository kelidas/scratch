
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List, Interface, implements, \
    Either, Enum, String
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, HGroup, OKButton, CodeEditor, \
        VGroup, HSplit, EnumEditor, Handler, SetEditor, EnumEditor
import subprocess
import multiprocessing
import os
import re
import wx
from numpy import loadtxt, diff, exp, log, array, arange, abs, sqrt, argmax, piecewise
from mpl_figure_editor import MPLFigureEditor

from matplotlib.figure import Figure
from scipy.optimize import fsolve
from scipy import interpolate
import numpy as np
import platform
import time
from either_type import EitherType
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from scipy.optimize import leastsq
from database_prep import res_lst, DATABASE_DIR
from mp_settings import MPF_ONE
import mpmath as mp
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from threading import Thread

# ===============================================================================
# Data Viewer
# ===============================================================================

class DirHandler(Handler):
    m_dirs = List(Str)
    n_dirs = List(Str)

    def object_database_dir_changed(self, info):
        self.m_dirs = os.listdir(info.object.database_dir)
        # As default value, use the first value in the list:
        info.object.m_dir = self.m_dirs[0]
        info.object.m_dirs = self.m_dirs

    def object_m_dir_changed(self, info):
        self.n_dirs = os.listdir(os.path.join(info.object.database_dir, info.object.m_dir))
        # As default value, use the first value in the list:
        self.n_dirs.sort()
        info.object.n_dir = self.n_dirs[0]
        info.object.n_dirs = self.n_dirs

class DirSelector(HasTraits):

    database_dir = Directory(DATABASE_DIR)
    m_dirs = List(Str)
    n_dirs = List(Str)
    m_dir = Str()
    n_dir = Str()

    n_dir_enabled = Property(Bool)
    def _get_n_dir_enabled(self):
        if self.options_ == 0:
            return True
        else:
            return False

    options = Trait('one number', {'one number':0,
                                  'one shape':1,
                                  'all':2})


    traits_view = View(
                       Item('database_dir', id='dir_selector.database_dir'),
                       Item('m_dir', editor=EnumEditor(name='handler.m_dirs'), id='dir_selector.m_dir'),
                       Item('options', style='custom', id='dir_selector.options'),
                       Item('n_dir', editor=EnumEditor(name='handler.n_dirs'), enabled_when='n_dir_enabled', id='dir_selector.n_dir'),
                      handler=DirHandler,
                       id='dir_selector.main'
                       )

class RecursionData(HasTraits):

    n_dir_lst = List
    m_dir_lst = List

    shape = List

    scale = Float(1.0, readonly=True)

    number_of_filaments = List

    x = List(Array)
    ln_x = List(Array)
    gn_cdf = List(Array)
    norm_cdf = List(Array)
    weibr_cdf = List(Array)
    weibl_cdf = List(Array)
    gn_wp = List(Array)
    norm_wp = List(Array)
    weibr_wp = List(Array)
    weibl_wp = List(Array)
    x_diff = List(Array)
    ln_x_diff = List(Array)
    gn_diff = List(Array)
    norm_diff = List(Array)

    dn = List
    sn = List

class PlotHandler(Handler):
    n_dirs = List(Str)
    m_dirs = List(Str)

    def object_load_options_changed(self, info):
        if info.object.m_dir_lst != []:
            self.m_dirs = info.object.m_dir_lst

    def object_m_selected_changed(self, info):
        n_dirs = []
        if info.object.n_dir_lst != []:
            for i in info.object.m_selected:
                idx = np.where((np.array(info.object.m_dir_lst) == i) == True)
                if list(idx) != []:
                    n_dirs += list(np.array(info.object.n_dir_lst)[idx])
            self.n_dirs = n_dirs

class PlotSelector(HasTraits):
    data = Instance(RecursionData)

    n_dir_lst = List(Str)
    m_dir_lst = List(Str)

    load_options = Button
    def _load_options_fired(self):
        self.n_selected = []
        self.m_selected = []
        self.n_dir_lst = self.data.n_dir_lst
        self.m_dir_lst = self.data.m_dir_lst

    m_selected = List()

    n_selected = List()

    plot_list = Property(List)
    def _get_plot_list(self):
        lst = []
        for i in self.m_selected:
            for j in self.n_selected:
                l = list(np.argwhere(
                                np.logical_and(np.array(self.data.m_dir_lst) == i,
                                               np.array(self.data.n_dir_lst) == j) == True))
                if l != []:
                    lst.append(int(l[0]))
        return lst

    traits_view = View(
                       Item('load_options', show_label=False, id='plot_selector.load_options'),
                       Item('m_selected', show_label=False,
                            editor=SetEditor(
                                          name='handler.m_dirs',
                                          # ordered=True,
                                          can_move_all=True,
                                          left_column_title='Available shapes',
                                          right_column_title='Selected shapes'), id='plot_selector.m_selected'),
                       Item('n_selected', show_label=False,
                            editor=SetEditor(
                                           name='handler.n_dirs',
                                           # ordered=True,
                                           can_move_all=True,
                                           left_column_title='Available numbers',
                                           right_column_title='Selected numbers'), id='plot_selector.n_selected'),
                       handler=PlotHandler,
                       id='plot_selector.main'
                     )

class BasePlot(HasTraits):

    name = 'base plot'

    data = Instance(RecursionData)

    plot_list = List

    figure = Instance(Figure)

    plot_selector = Instance(PlotSelector)

    clear_on = Bool(True)

    draw = Button()

    def _draw_fired(self):
        axes = self.figure.axes[0]
        if self.clear_on:
            axes.clear()
        axes.set_title(self.name)
        axes.plot([1, 2, 3], [1, 2, 2])
        # wx.CallAfter(self.figure.canvas.draw)
        self.figure.canvas.draw()

    traits_view = View(
                       'clear_on',
                       Item('draw', show_label=False),
                       id='plot.main'
                       )

class WPPlot(BasePlot):

    name = 'Weibull plot'
    gn_on = Bool(True)
    norm_on = Bool(True)
    weibl_on = Bool(True)
    weibr_on = Bool(True)

    def _draw_fired(self):
        axes = self.figure.axes[0]
        if self.clear_on:
            axes.clear()
        axes.set_title(self.name)
        for i in self.plot_selector.plot_list:
            if self.gn_on:
                x = self.data.ln_x[i]
                y = self.data.gn_wp[i]
                axes.plot(x, y, 'k-')
            if self.norm_on:
                x = self.data.ln_x[i]
                y = self.data.norm_wp[i]
                axes.plot(x, y, 'b-')
            if self.weibl_on:
                x = self.data.ln_x[i]
                y = self.data.weibl_wp[i]
                axes.plot(x, y, 'g-')
            if self.weibr_on:
                x = self.data.ln_x[i]
                y = self.data.weibr_wp[i]
                axes.plot(x, y, 'g-')
        def form3(x, pos):
            mp.mp.dps = 1000
            return '%s %%' % mp.nstr((MPF_ONE - mp.exp(-mp.exp(x))) * 100, 6)
        formatter = FuncFormatter(form3)
        axes.yaxis.set_major_formatter(FuncFormatter(formatter))
        axes.set_xlabel('log(x)')
        axes.set_ylabel('probability [log(-log(1-cdf))]')

        self.figure.canvas.draw()

    traits_view = View(
                       'clear_on',
                       Group(
                             'gn_on',
                             'norm_on',
                             'weibl_on',
                             'weibr_on',
                             show_border=True,
                             label='data select',
                             ),
                       Item('draw', show_label=False),
                       id='plot.main'
                       )

class DiffPlot(BasePlot):

    name = 'Differential of Weibull plot'
    gn_on = Bool(True)
    norm_on = Bool(True)

    def _draw_fired(self):
        axes = self.figure.axes[0]
        if self.clear_on:
            axes.clear()
        axes.set_title(self.name)
        for i in self.plot_selector.plot_list:
            if self.gn_on:
                x = self.data.ln_x_diff[i]
                y = self.data.gn_diff[i]
                axes.plot(x, y, 'k-')
            if self.norm_on:
                x = self.data.ln_x_diff[i]
                y = self.data.norm_diff[i]
                axes.plot(x, y, 'b-')
        axes.set_xlabel('log(x)')
        axes.set_ylabel('diff(log(x),log(-log(1-cdf)))')

        self.figure.canvas.draw()

    traits_view = View(
                       'clear_on',
                       Group(
                             'gn_on',
                             'norm_on',
                             show_border=True,
                             label='data select',
                             ),
                       Item('draw', show_label=False),
                       id='plot.main'
                       )


class LAPlot(BasePlot):

    name = 'Left assymptot params plot'

    var_sel = Enum('dn', 'sn')

    def _draw_fired(self):
        axes = self.figure.axes[0]
        if self.clear_on:
            axes.clear()
        axes.set_title(self.name)
        yn = []
        n = []
        for i in self.plot_selector.plot_list:
            yn.append(mp.log(getattr(self.data, self.var_sel)[i].reshape(1)[0]))
            n.append(self.data.number_of_filaments[i])
        axes.plot(n, yn, 'k-x')
        axes.set_xlabel('number of filaments')
        axes.set_ylabel('log(%s)' % self.var_sel)

        self.figure.canvas.draw()

    traits_view = View(
                       'clear_on',
                       Group(
                             Item('var_sel', style='custom', show_label=False),
                             show_border=True,
                             label='data select',
                             ),
                       Item('draw', show_label=False),
                       id='plot.main'
                       )


class PDFPlot(BasePlot):
    name = 'PDF plot'
    gn_on = Bool(True)
    norm_on = Bool(True)
    weibl_on = Bool(False)
    weibr_on = Bool(False)

    def _draw_fired(self):
        axes = self.figure.axes[0]
        if self.clear_on:
            axes.clear()
        axes.set_title(self.name)
        for i in self.plot_selector.plot_list:
            if self.gn_on:
                x = (self.data.x[i][1:] + self.data.x[i][:-1]) / 2.
                dx = (self.data.x[i][1:] - self.data.x[i][:-1])
                y = ((self.data.gn_cdf[i][ 1:] - self.data.gn_cdf[i][:-1]) / dx)
                axes.plot(x, y, 'k-')
            if self.norm_on:
                x = (self.data.x[i][1:] + self.data.x[i][:-1]) / 2.
                dx = (self.data.x[i][1:] - self.data.x[i][:-1])
                y = ((self.data.norm_cdf[i][ 1:] - self.data.norm_cdf[i][:-1]) / dx)
                axes.plot(x, y, 'b-')
            if self.weibl_on:
                x = (self.data.x[i][1:] + self.data.x[i][:-1]) / 2.
                dx = (self.data.x[i][1:] - self.data.x[i][:-1])
                y = ((self.data.weibl_cdf[i][ 1:] - self.data.weibl_cdf[i][:-1]) / dx)
                axes.plot(x, y, 'g-')
            if self.weibr_on:
                x = (self.data.x[i][1:] + self.data.x[i][:-1]) / 2.
                dx = (self.data.x[i][1:] - self.data.x[i][:-1])
                y = ((self.data.weibr_cdf[i][ 1:] - self.data.weibr_cdf[i][:-1]) / dx)
                axes.plot(x, y, 'g-')

        self.figure.canvas.draw()

    traits_view = View(
                       'clear_on',
                       Group(
                             'gn_on',
                             'norm_on',
                             'weibl_on',
                             'weibr_on',
                             show_border=True,
                             label='data select',
                             ),
                       Item('draw', show_label=False),
                       id='plot.main'
                       )


class LoadThread(Thread):

    wants_abort = False

    def run(self):
        if self.selector.options_ == 0:
            if self.selector.n_dir in self.data.n_dir_lst:
                self.load_info_display(self.selector.m_dir + ', ' + self.selector.n_dir + ', yet loaded')
                return
            self.load_info_display(self.selector.m_dir + ', ' + self.selector.n_dir)
            self.__load_n_data(self.selector.m_dir, self.selector.n_dir)
            self.data.n_dir_lst.append(self.selector.n_dir)
            self.load_info_display('Finished!')
        elif  self.selector.options_ == 1:
            for d in self.selector.n_dirs:
                if self.wants_abort == False:
                    if d in self.data.n_dir_lst:
                        self.load_info_display(self.selector.m_dir + ', ' + d + ', yet loaded')
                        continue
                    self.load_info_display(self.selector.m_dir + ', ' + d)
                    self.__load_n_data(self.selector.m_dir, d)
                    self.data.n_dir_lst.append(d)
            self.load_info_display('Finished!')
        else:
            for m in self.selector.m_dirs:
                if self.wants_abort == False:
                    self.selector.m_dir = m
                    for d in self.selector.n_dirs:
                        if d in self.data.n_dir_lst:
                            self.load_info_display(m + ', ' + d + ', yet loaded')
                            continue
                        self.load_info_display(m + ', ' + d)
                        self.__load_n_data(m, d)
                        self.data.n_dir_lst.append(d)
            self.load_info_display('Finished!')

    def __load_n_data(self, m_dirname, n_dirname):
        m = re.match(r'n=(?P<number>\d+)_m=(?P<shape>\d+.\d+)', n_dirname)
        m = m.groupdict()
        self.data.shape.append(float(m['shape']))
        self.data.number_of_filaments.append(int(m['number']))
        for res in res_lst:
            data = (np.load(os.path.join(self.selector.database_dir,
                                             m_dirname, n_dirname,
                                             n_dirname + '-%s.npy' % res)))
            getattr(self.data, res).append(data)
            data = []
        self.data.m_dir_lst.append('m=%05.1f' % float(m['shape']))

class ControlPanel(HasTraits):

    load_info = String()

    data = Instance(RecursionData, ())
    selector = Instance(DirSelector, ())

    plot_selector = Instance(PlotSelector)
    def _plot_selector_default(self):
        return PlotSelector(data=self.data)

    @on_trait_change('data')
    def _plot_selector_deflt(self):
        return PlotSelector(data=self.data)

    plot = EitherType(names=['wp plot',
                             'pdf plot',
                             'diff_plot',
                             'left asympt. params plot',
                             'base',
                             ],
                      klasses=[WPPlot,
                               PDFPlot,
                               DiffPlot,
                               LAPlot,
                               BasePlot,
                               ])

    def _plot_default(self):
        return WPPlot(data=self.data, figure=self.figure, plot_selector=self.plot_selector)

    @on_trait_change('plot')
    def _plot_deflt(self):
        self.plot.data = self.data
        self.plot.figure = self.figure
        self.plot.plot_selector = self.plot_selector

    load_thread = Instance(LoadThread)

    start_stop_loading = Button('Start/Stop loading')

    def _start_stop_loading_fired(self):
        if self.load_thread and self.load_thread.isAlive():
            self.load_thread.wants_abort = True
        else:
            self.load_thread = LoadThread()
            self.load_thread.load_info_display = self._add_line
            self.load_thread.data = self.data
            self.load_thread.selector = self.selector
            self.load_thread.start()

    def _add_line(self, string):
        """ Adds a line to the textbox display.
        """
        self.load_info = (string + '\n' + self.load_info)[0:1000]

    traits_view = View(
                       Group(
                             Item('selector@', show_label=False),
                             Item('start_stop_loading', show_label=False),
                             Group(
                             Item('load_info', show_label=False, style='custom'),
                             label='Load info', show_border=True
                             ),
                             label='load control',
                             dock='tab', id='control_panel.load_control'),
                       Group(
                             Item('plot_selector', show_label=False, style='custom'),
                             label='plot selector',
                             dock='tab',
                             id='control_panel.plot_selector',
                       ),
                       Group(
                             Item('plot', style='custom', show_label=False),
                             label='plot control',
                             dock='tab',
                             id='control_panel.plot',
                       ),
                       id='control_panel.main'
                       )


class MainWindow(HasTraits):

    figure = Instance(Figure)

    panel = Instance(ControlPanel)

    def _panel_default(self):
        return ControlPanel(figure=self.figure)

    def _figure_default(self):
        figure = Figure(tight_layout=True)
        figure.add_subplot(111)
        # figure.add_axes([0.2, 0.04, 0.7, 0.8])
        return figure

    view = View(HSplit(
                       Item('panel', style='custom', show_label=False,
                            id='main_window.panel'),
                       Item('figure', editor=MPLFigureEditor(), show_label=False,
                            dock='tab', id='main_window.figure'),
                       id='main_window.hsplit',
                       ),
                title='Recursion Analyzer',
                id='main_window.view',
                resizable=True,
                height=0.5, width=0.75,
                buttons=[OKButton],
                )



app = MainWindow()
app.configure_traits()



exit()



if __name__ == '__main__':

    def gen_data_all():
        all_dirs = False
        if all_dirs:
            dirname = os.path.dirname(data.inputfile)[:-6]
            dirs = ['m=3.00', 'm=4.00', 'm=5.00', 'm=6.00', 'm=7.00', 'm=8.00',
                    'm=9.00', 'm=10.00', 'm=15.00']
        else:
            dirname = os.path.dirname(data.inputfile)
            dirs = ['.']
        for dirn in dirs:
            files = [v for v in os.listdir(os.path.join(dirname, dirn)) if os.path.splitext(v)[1] == ".txt"]
            for f in files:
                d = Data(inputfile=os.path.join(dirname, dirn, f))
                x = (d.ln_x[:-1] + d.ln_x[1:]) / 2.0
                y = d.wp_cdf_x
                # y = tan_log(d.x, d.number_of_filaments, d.scale, d.shape, 1)
                # y = (differentiate(d.ln_x, y))
                y = (differentiate(d.ln_x, y) - d.shape) / (d.shape * d.number_of_filaments - d.shape)
                yy = d.wp_gauss_x
                yy = (differentiate(d.ln_x, yy) - d.shape) / (d.shape * d.number_of_filaments - d.shape)
                plt.plot(x, y)
                plt.plot(x, yy, 'c.')
        plt.plot(x, y, linewidth=2)
        # plt.legend(loc=0)
        plt.show()




# plt.figure(4)
# plt.title('integ')
# y_lst = [83.58,56.4,36.1,16.9]
#
# for idx,val in enumerate(dk):
#    y = tan_log(xx, n, scale, shape, 1)
#    y2=der_(x,y) + (n-idx-1)*shape
#    x2=(x[:-1]+x[1:])/2. - x_pos[int(n)-idx-1]
#    integ = diff(x2) * (y2[1:]+y2[:-1])/2.
#    integ = cumsum(integ)
#    plt.plot((x2[:-1]+x2[1:])/2., integ-y_lst[idx], 'g-', linewidth = 3, label='int_tan')
