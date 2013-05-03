from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton, CodeEditor, VGroup, HSplit
import subprocess
import multiprocessing
import os
import re
from numpy import loadtxt, diff, exp, log, array, arange, abs, sqrt, argmax, piecewise
from scipy.misc import comb
from mpl_figure_editor import MPLFigureEditor
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy.optimize import fsolve
from scipy import interpolate
import numpy as np
import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from scipy.optimize import leastsq
from matplotlib.ticker import FuncFormatter

def tan_(x, dk, scale, shape, k):
    z = (dk * (x / scale) ** (k * shape))
    ret = piecewise(z,
                    [z < 0, z <= 10 ** (-12), z > 10 ** (-12)],
                     [lambda z: 0, lambda z: z - 0.5 * z * z + 1 / 6. * z ** 3 - 1 / 24. * z ** 4, lambda z: 1. - exp(-z) ])
    return piecewise(ret,
                      [ret <= 10 ** (-12), ret > 10 ** (-12)],
                      [lambda ret: log(ret), lambda ret: log(-log(1 - ret)) ])

def tan_log(x, dk, scale, shape, k):
    z = (dk * (x / scale) ** (k * shape))
    ret = piecewise(z,
                    [z <= 10 ** (-12), z > 10 ** (-12)],
                    [lambda z: z - 0.5 * z * z, lambda z: 1. - exp(-z) ])
    return piecewise(ret,
                     [ret <= 10 ** (-12), ret > 10 ** (-12)],
                     [lambda ret: log(ret), lambda ret: log(ret) ])

def _dn(n, shape):
    ret = 0.
    if n < 1:
        return 1.0
    elif n == 1:
        return 1.0
    else:
        for k in range(1, n):
            ret += (-1) ** (k + 1) * comb(n, k) * (n / float(n - k)) ** (shape * (n - k)) * _dn(n - k, shape)
        return (-1) ** (n + 1) + ret

def dist(q, xp, yp, x0=0., y0=0.):
    # y - y0 = k (x - x0)
    dist = abs(yp - y0 - q * (xp - x0)) / sqrt(1 * 1 + q * q)
    return dist

def tan_min(dk, x, y, k, scale, shape):
    return tan_(x, dk, scale, shape, k) - y

def tan_pos(x, y, dist, k, scale, shape):
    idx = argmax(dist)
    return fsolve(tan_min, 1., args=(x[idx], y[idx], k, scale, shape))[0]

def Kr(r):
    return 1 + r / 2.0

def _dk(k, shape):
    res = 1.0
    for i in range(1, k):
        res *= Kr(i)
    return 2 ** (k - 1) * res ** shape

def differentiate(x, y):
    return np.diff(y) / np.diff(x)

def an(k):
    return (N * _dk(k)) ** (-1.0 / (k * shape))

def H(k, x):
    z = (x / an(k)) ** (k * shape)
    ret = piecewise(z, [z <= 10 ** (-12), z > 10 ** (-12)], [lambda z: z - 0.5 * z * z, lambda z: 1. - exp(-z) ])
    return piecewise(ret, [ret <= 10 ** (-12), ret > 10 ** (-12)], [lambda ret: log(ret), lambda ret: log(ret) ])

#===============================================================================
# Data Viewer
#===============================================================================

class Data(HasTraits):
    inputfile = File(filter=['*.txt'])

    shape = Float

    scale = Float(1.0, readonly=True)

    number_of_filaments = Int

    data = Array

    x = Array
    cdf_x = Array
    gauss_x = Array
    weibl_x = Array
    weibr_x = Array
    ln_x = Array
    wp_cdf_x = Array
    wp_gauss_x = Array
    wp_weibl_x = Array
    wp_weibr_x = Array

    dn = Float
    dk = List

    tan_on = Bool(False, data_changed=True)

    def _inputfile_changed(self):
        name = os.path.basename(self.inputfile)[:-4]
        self.shape = float(self.__get_shape_number(name)['shape'])
        self.number_of_filaments = int(self.__get_shape_number(name)['number'])
        self.data = self.__load_data(self.inputfile)
        self.x = self.data[:, 0]
        self.cdf_x = self.data[:, 1]
        self.gauss_x = self.data[:, 2]
        self.weibl_x = self.data[:, 3]
        self.weibr_x = self.data[:, 4]
        self.ln_x = self.data[:, 5]
        self.wp_cdf_x = self.data[:, 6]
        self.wp_gauss_x = self.data[:, 7]
        self.wp_weibl_x = self.data[:, 8]
        self.wp_weibr_x = self.data[:, 9]
#        if os.path.exists(self.inputfile[:-4] + '_dn.npy'):
#            self.dn = float(np.load(self.inputfile[:-4] + '_dn.npy'))
#        else:
#            self.dn = _dn(self.number_of_filaments, self.shape)
#            np.save(self.inputfile[:-4] + '_dn.npy', self.dn)
#        if os.path.exists(self.inputfile[:-4] + '_dk.npy'):
#            self.dk = np.load(self.inputfile[:-4] + '_dk.npy').tolist()
#        else:
#            self.dk = [self.number_of_filaments]
#            for k in range(2, self.number_of_filaments):
#                x = self.ln_x
#                y = self.wp_cdf_x
#                dd = dist((self.shape * k), x, y, 0, -100000)
#                self.dk.append(tan_pos(self.x, y, dd, k, self.scale, self.shape))
#            self.dk.append(self.dn)
#            print self.dk
#            np.save(self.inputfile[:-4] + '_dk.npy', np.array(self.dk))

    def __get_shape_number(self, name):
        m = re.match(r'm=(?P<shape>\d+.\d+)_n=(?P<number>[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)', name)
        return m.groupdict()

    def __load_data(self, infile):
        # start_t = sysclock()
        if os.path.exists(infile[:-4] + '.npy'):
            data = np.load(infile[:-4] + '.npy')
        else:
            data = np.loadtxt(infile, skiprows=5, dtype=np.float64)
            np.save(infile[:-4] + '.npy', data)
        # print 'data loaded', 'time =', sysclock() - start_t
        return data

    traits_view = View(
            Item('inputfile'),
               Item('inputfile', style='custom'),
               Item('shape', style='readonly'),
               Item('scale', style='readonly'),
               Item('number_of_filaments', style='readonly'),
               Item('tan_on'),)

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
