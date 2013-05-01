
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List, Interface, implements, Either
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, HGroup, OKButton, CodeEditor, VGroup, HSplit, EnumEditor, Handler
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
from util.traits.either_type import EitherType
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from scipy.optimize import leastsq
from database_prep import res_lst, DATABASE_DIR


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
    n_dir_on = Bool(True)

    traits_view = View(
                       Item('database_dir'),
                       Item('m_dir', editor=EnumEditor(name='handler.m_dirs')),
                       Item('n_dir_on'),
                       Item('n_dir', editor=EnumEditor(name='handler.n_dirs'), enabled_when='n_dir_on'),
                       handler=DirHandler
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

class BasePlot(HasTraits):
    data = Instance(RecursionData)

    figure = Instance(Figure)

    n_dir_lst = DelegatesTo('data')
    m_dir_lst = DelegatesTo('data')

    n_plot_on = Bool(True)

    draw = Button()

    def _draw_fired(self):
        figure = self.figure
        axes = figure.axes[0]
        axes.clear()
        axes.plot([1, 2], [1, 2])
        wx.CallAfter(self.figure.canvas.draw)

    traits_view = View(
                       'n_plot_on',
                       Item('draw', show_label=False)
                       )

class WPPlot(BasePlot):
    def _draw_fired(self):
        figure = self.figure
        axes = figure.axes[0]
        axes.clear()
        x = np.array(self.data.ln_x[0], dtype=np.float64)
        y = np.array(self.data.gn_wp[0], dtype=np.float64)
        axes.plot(x, y, 'b-')
        wx.CallAfter(self.figure.canvas.draw)

    traits_view = View(
                       'n_plot_on',
                       Item('draw', show_label=False)
                       )

class ControlPanel(HasTraits):

    data = Instance(RecursionData, ())
    selector = Instance(DirSelector, ())
    figure = Instance(Figure)
    plot = EitherType(names=['base',
                             'wp plot'],
                      klasses=[BasePlot,
                               WPPlot])
    def _plot_default(self):
        return BasePlot(data=self.data, figure=self.figure)

    @on_trait_change('plot')
    def _plot_deflt(self):
        self.plot.data = self.data
        self.plot.figure = self.figure

    load_data = Button()

    def _load_data_fired(self):
        if self.selector.n_dir_on:
            print self.selector.n_dir
            self.__load_n_data(self.selector.n_dir)
            self.data.n_dir_lst.append(self.selector.n_dir)
        else:
            for d in self.selector.n_dirs:
                print d
                self.__load_n_data(d)
                self.data.n_dir_lst.append(d)

    def __load_n_data(self, n_dirname):
        m = re.match(r'n=(?P<number>\d+)_m=(?P<shape>\d+.\d+)', n_dirname)
        m = m.groupdict()
        self.data.shape.append(float(m['shape']))
        self.data.number_of_filaments.append(int(m['number']))
        data = []
        for res in res_lst:
            data.append(np.load(os.path.join(self.selector.database_dir,
                                             self.selector.m_dir, n_dirname,
                                             n_dirname + '-%s.npy' % res)))
            getattr(self.data, res).append(data)
            data = []
        self.data.m_dir_lst.append('m=%05.1f' % float(m['shape']))

    traits_view = View(
                       Group(
                             Item('selector@', show_label=False),
                             Item('load_data', show_label=False),
                             dock='tab',
                             label='load data'),
                       Group(
                             Item('plot', style="custom", dock='tab', show_label=False),
                             label='plot control'
                       )
                       )


class MainWindow(HasTraits):

    figure = Instance(Figure)

    panel = Instance(ControlPanel, ())

    def _figure_default(self):
        figure = Figure()
        figure.add_axes([0.05, 0.04, 0.9, 0.92])
        return figure

    def _panel_default(self):
        return ControlPanel(figure=self.figure)

    view = View(HSplit(
                       Item('panel', style='custom', show_label=False),
                       Item('figure', editor=MPLFigureEditor(),
                            dock='vertical', show_label=False),
                      ),
                resizable=True,
                # height=0.75, width=0.75
                )



data = MainWindow()
data.configure_traits()

exit()


class DataViewer(HasTraits):
    data_inst = Instance(Data, ())

    inputfile = DelegatesTo('data_inst')

    shape = DelegatesTo('data_inst')

    scale = DelegatesTo('data_inst')

    number_of_filaments = DelegatesTo('data_inst')

    data = DelegatesTo('data_inst')

    x = DelegatesTo('data_inst')
    cdf_x = DelegatesTo('data_inst')
    gauss_x = DelegatesTo('data_inst')
    weibl_x = DelegatesTo('data_inst')
    weibr_x = DelegatesTo('data_inst')
    ln_x = DelegatesTo('data_inst')
    wp_cdf_x = DelegatesTo('data_inst')
    wp_gauss_x = DelegatesTo('data_inst')
    wp_weibl_x = DelegatesTo('data_inst')
    wp_weibr_x = DelegatesTo('data_inst')

    dn = DelegatesTo('data_inst')
    dk = DelegatesTo('data_inst')

    tan_on = DelegatesTo('data_inst')

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        figure.add_axes([0.1, 0.1, 0.8, 0.8])
        return figure

    data_changed = Event(True)

    @on_trait_change('inputfile, tan_on, data_inst. +data_changed')
    def _redraw(self):
        figure = self.figure
        axes = figure.axes[0]
        axes2 = axes.twinx()
        axes.clear()
        axes2.clear()

        def prevod(y):
            return 1 - exp(-exp(y))

        def update_axes2(axes):
            y1, y2 = axes.get_ylim()
            a = axes.get_xticks()
            # axes2.set_ylim(prevod(y1), prevod(y2))
            axes2.set_yticks(prevod(a))
            axes2.figure.canvas.draw()

        axes.callbacks.connect("ylim_changed", update_axes2)
        axes2.set_ylabel('prob')
        axes.plot(self.ln_x, self.wp_cdf_x, 'b-', linewidth=2, label='cdf_x')
        axes.plot(self.ln_x, self.wp_gauss_x, 'g-', linewidth=1, label='gauss_x')
        axes.plot(self.ln_x, self.wp_weibl_x, 'r-', linewidth=1, label='weibl_x')
        axes.plot(self.ln_x, self.wp_weibr_x, 'r-', linewidth=1, label='weibr_x')
        if self.tan_on:
            for idx, val in enumerate(self.dk):
                label = None
                if idx == 0:
                    label = 'tan'
                axes.plot(self.ln_x, tan_(self.x, val, self.scale, self.shape,
                                          idx + 1),
                          color='grey', label=label)
        axes.grid()
        axes.legend(loc=0)
        axes.set_xlabel('x')
        axes.set_ylabel('y')

        self.data_changed = True

    traits_view = View(
                    HSplit(
                    VGroup(
                   Item('data_inst@', show_label=False),
                   label='Config',
                   id='data_inst',
                   dock='tab',
                   ),
                    VGroup(
                   Item('figure', editor=MPLFigureEditor(), show_label=False),
                   label='Plot sheet',
                    id='plot',
                    dock='tab',
                   ),
                           ),
                    title='DataViewer',
                    id='view',
                    dock='tab',
                    resizable=True,
                    width=.5,
                    height=.5,
                    buttons=[OKButton])

if __name__ == '__main__':
    viewer = DataViewer()
    viewer.configure_traits()

    data = viewer.data_inst
    print data.shape

    def fit_data():
        # FIT data
        def f(a, b, c, d):
            z = (1 - np.exp(-(x / (a)) ** (b))) ** (c)
            ret = piecewise(z,
                        [z < 0, z <= 10 ** (-12), z > 10 ** (-12)],
                         [lambda z: 0, lambda z: z - 0.5 * z * z + 1 / 6. * z ** 3 - 1 / 24. * z ** 4, lambda z: 1. - exp(-z) ])
            return piecewise(ret,
                              [ret <= 10 ** (-12), ret > 10 ** (-12)],
                              [lambda ret: log(ret) + data.wp_cdf_x.max(), lambda ret: log(-log(1 - ret)) + data.wp_cdf_x.max()])
            # return np.log(-np.log(1 - np.exp(-(x / s) ** (6 * a)) ** (3 * b)))

        def residuals(p, y, x):
            err = y - f(*p)
            return err

        p0 = [ 1., 1., 1., 1.]
        from scipy.optimize import leastsq
        x = data.x
        y = data.wp_cdf_x
        plsq = leastsq(residuals, p0, args=(y, data.ln_x), ftol=1.49012e-12, xtol=1.49012e-12, maxfev=100000)
    #    np.savetxt('x.txt', data.x)
    #    np.savetxt('lnx.txt', data.x)
    #    np.savetxt('wpcdfx.txt', data.wp_cdf_x)
        print 'plsq', plsq
        # np.save(data.inputfile[:-4] + '_plsq.npy', plsq[0])
        plt.figure(0)
        plt.plot(data.ln_x, y)
        plt.plot(data.ln_x, f(*plsq[0]))

        plt.show()

    def plot_derivation():
        # derivation
        plt.figure(1)
        plt.title('deriv_1')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.cdf_x)), label='cdf_x')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.gauss_x)), label='gauss')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.weibl_x)), label='weibl')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.weibr_x)), label='weibr')

        for idx, val in enumerate(data.dk):
            label = None
            if idx == 0:
                label = 'tan'
            y = tan_log(data.x, val, data.scale, data.shape, idx + 1)
            plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, y), color='black', label=label)
        plt.legend()

        plt.figure(2)
        plt.title('deriv_2')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.cdf_x)), label='cdf_x')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.gauss_x)), label='gauss')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.weibl_x)), label='weibl')
        plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, log(data.weibr_x)), label='weibr')

        x_pos = [0, 0.28, 0.6, 1.16]
        y = tan_log(data.x, data.number_of_filaments, data.scale, data.shape, 1)
        f_cdf = interpolate.interp1d(differentiate(data.ln_x, log(data.cdf_x))[::-1], ((data.ln_x[:-1] + data.ln_x[1:]) / 2.)[::-1])
        f_y = interpolate.interp1d(differentiate(data.ln_x, log(data.weibr_x))[::-1], ((data.ln_x[:-1] + data.ln_x[1:]) / 2.)[::-1])
        for idx, val in enumerate(data.dk):
            label = None
            if idx == 0:
                label = 'tan'
            pos_x = f_cdf(data.shape * (idx + 0.5)) - f_y(data.shape / 2.)
            pos_y = data.shape * idx
            plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2. + pos_x, differentiate(data.ln_x, y) + pos_y, color='black', label=label)
    #    plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2., differentiate(data.ln_x, y), color='black', label='tan%i' % 1)
    #    plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2. - 0.28, differentiate(data.ln_x, y) + 6, color='black', label='tan%i' % 2)
    #    plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2. - 0.6, differentiate(data.ln_x, y) + 12, color='black', label='tan%i' % 3)
    #    plt.plot((data.ln_x[:-1] + data.ln_x[1:]) / 2. - 1.16, differentiate(data.ln_x, y) + 18, color='black', label='tan%i' % 4)
        plt.legend()


        plt.show()

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

    def fit_data_diff():
        # FIT data
        def f_weib(a, b):
            z = (x / a) ** b
            return piecewise(z,
                    [z < 0, z <= 10 ** (-12), z > 10 ** (-12)],
                     [lambda z: 0, lambda z: z - 0.5 * z * z + 1 / 6. * z ** 3 - 1 / 24. * z ** 4, lambda z: 1. - exp(-z) ])

        def f_gumb(a, b):
            return np.exp(-np.exp(-(-x - a) / b))

        def f_gev(a, b, c):
            return np.exp(-(1 + a * ((-x - b) / c)) ** (-1.0 / a))

        def residuals(p, y, x):
            err = y - f_gumb(*p)
            return err

        p0 = [1., 1.]
        xx = (data.ln_x[:-1] + data.ln_x[1:]) / 2.0
        y = data.wp_cdf_x
        y = (differentiate(data.ln_x, y) - data.shape) / (data.shape * data.number_of_filaments - data.shape)
        # y = f(3, 6)
        mask = xx < -.3
        x = xx[mask]
        y = y[mask]
        plsq = leastsq(residuals, p0, args=(y, x))  # , ftol=1.49012e-12, xtol=1.49012e-12, maxfev=10000)
        yy = data.wp_gauss_x
        yy = (differentiate(data.ln_x, yy) - data.shape) / (data.shape * data.number_of_filaments - data.shape)
    #    np.savetxt('x.txt', data.x)
    #    np.savetxt('lnx.txt', data.x)
    #    np.savetxt('wpcdfx.txt', data.wp_cdf_x)
        print 'plsq', plsq
        # np.save(data.inputfile[:-4] + '_plsq.npy', plsq[0])
        plt.figure(0)
        plt.plot(x, y, 'k-')
        plt.plot(xx, yy, 'g--', linewidth=.5)
        plt.plot(x, f_gumb(*plsq[0]), 'r')

        plt.show()


    # fit_data()
    # plot_derivation()
    gen_data_all()
    fit_data_diff()




































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
