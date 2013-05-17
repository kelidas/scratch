import numpy as np
import os
from scratch.recursion.database_prep import res_lst
import numpy as np
from traits.api import HasTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton, CodeEditor, VGroup, HSplit
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import shutil
import mpmath as mp
from scratch.recursion.database_prep import DATABASE_DIR

mp.mp.dps = 1000

class Selector(HasTraits):

    d = Directory(auto_set=False)

    name = Str()
    @on_trait_change('d')
    def _part_name(self):
        self.name = os.path.split(self.d)[1]

    traits_view = View(
                    Item('d', style='custom'),
                    title='Directory Selector',
                    id='database_select',
                    dock='tab',
                    resizable=True,
                    width=.5,
                    height=.5,
                    buttons=[OKButton])

def load_subdir_lists(dir_name):
    name_lst = []
    path_lst = []
    for path, subdirs, files in os.walk(dir_name):
        for name in subdirs:
            name_lst.append(name)
            path_lst.append(path)
    return name_lst, path_lst

def loadplot_data(part_name):
    ln_x_diff = np.load(part_name + '-ln_x_diff.npy')

    gn_diff = np.load(part_name + '-gn_diff.npy')
    norm_diff = np.load(part_name + '-norm_diff.npy')

    plt.figure(1)
    plt.plot(ln_x_diff, gn_diff, 'rx-')
    plt.plot(ln_x_diff, norm_diff, 'b-')
    plt.plot([-4.5, 1], [0, 0], 'k--')
    plt.plot([-4.5, 1], [1, 1], 'k--')
    plt.xlim(-4.5, 1)
    plt.ylim(-0.2, 1.2)

    x_limits = []

    plt.waitforbuttonpress()
    plt.title('click x1')
    x_limits.append(plt.ginput(1, 0)[0][0])
    plt.title('x1 clicked')
    plt.waitforbuttonpress()
    plt.title('click x2')
    x_limits.append(plt.ginput(1, 0)[0][0])
    plt.title('x2 clicked')

    mask = (ln_x_diff > x_limits[0]) * (ln_x_diff < x_limits[1])
    return mask

if __name__ == '__main__':
    from scratch.recursion.fn_lib import  weib_cdf_vect, norm_cdf_vect, weibul_plot_vect, differentiate, sn_mp, weibl_cdf_vect
    from scratch.recursion.fn_lib import fit_data_leastsq
    from scipy import stats
    s = Selector(d=os.path.join(DATABASE_DIR, 'm=010.0'))
    # s.configure_traits()

    def f_weib(x, a, b, c):
        '''CDF of the Weibull distribution reflected across the axis y.
        '''
        rv = stats.weibull_min(c, loc=a, scale=b)
        return rv.cdf(x)

    x = np.load(os.path.join(s.d, 'm=010.0_n=0004', 'm=010.0_n=0004' + '-x.npy')).astype(float)
    gn_cdf = np.load(os.path.join(s.d, 'm=010.0_n=0004', 'm=010.0_n=0004' + '-gn_cdf.npy')).astype(float)
    shape = 3.0
    n = 4.0
    y = (x ** (-shape) * np.log(-1 / (gn_cdf - 1))) ** (-1 / shape)
#     ys = np.log(-np.log((1 - gn_cdf))) / np.log(x / 1.0)
#     plt.plot(np.log(x), ys)
#     plt.show()

    yy = (1.0 / y ** ((shape))) / n
#     plt.figure(0)
#     plt.plot(np.log(x), y)

#     plt.figure(1)
#     plt.plot(x, y)

    y_fit, par = fit_data_leastsq(f_weib, x, yy)
    plt.figure(2)
    plt.plot(x, yy)
    plt.plot(x, y_fit)

    plt.figure(3)
    plt.plot(np.log(x - par[0][0]), weibul_plot_vect(yy))
    plt.plot(np.log(x - par[0][0]), weibul_plot_vect(y_fit))

    plt.figure(4)
    plt.plot(np.log(x), weibul_plot_vect(yy))
    plt.plot(np.log(x), weibul_plot_vect(y_fit))

#     plt.figure(3)
#     plt.plot(np.log(x), weibul_plot_vect(gn_cdf))
#     plt.plot(np.log(x), weibul_plot_vect(weib_cdf_vect(x, shape, y)))

    s = Selector(d=os.path.join(DATABASE_DIR, 'm=010.0'))
    x = np.load(os.path.join(s.d, 'm=010.0_n=0050', 'm=010.0_n=0050' + '-x.npy')).astype(float)
    gn_cdf = np.load(os.path.join(s.d, 'm=010.0_n=0050', 'm=010.0_n=0050' + '-gn_cdf.npy')).astype(float)
    shape = 3.0
    n = 50.0
    y = (x ** (-shape) * np.log(-1 / (gn_cdf - 1))) ** (-1 / shape)
    yy = (1.0 / y ** ((shape))) / n

    x = x[x <= 0.9]
    yy = yy[x <= 0.9]
    y_fit, par = fit_data_leastsq(f_weib, x, yy, p0=[0.5, 1.0, 1.0])
    print par

    plt.figure(2)
    plt.plot(x, yy)
    plt.plot(x, y_fit, 'k-')

    plt.figure(3)
    plt.plot(np.log(x - par[0][0]), weibul_plot_vect(yy))
    plt.plot(np.log(x - par[0][0]), weibul_plot_vect(y_fit))

    plt.figure(4)
    plt.plot(np.log(x), weibul_plot_vect(yy))
    plt.plot(np.log(x), weibul_plot_vect(y_fit))

    plt.show()

    # CHECK shape of data
#     subdir_lst, path_lst = load_subdir_lists(s.d)
#     outfile = open('check.txt', 'w')
#     for sub in subdir_lst:
#         outfile.write(sub + '\n')
#         for res in res_lst:
#             data = np.load(os.path.join(s.d, sub, sub + '-%s.npy' % res))
#             outfile.write('%s - %s\n' % (data.shape, res))
#             if data.shape == (50,):
#                 print data.shape, '--', res, sub
#         outfile.write('#######################################################\n')

    # fix database data
#     ln_x = np.load(os.path.join(s.d, 'm=011.0_n=0400', 'm=011.0_n=0400' + '-ln_x.npy'))
#     x = np.load(os.path.join(s.d, 'm=011.0_n=0400', 'm=011.0_n=0400' + '-x.npy'))
#     norm_cdf = np.load(os.path.join(s.d, 'm=011.0_n=0400', 'm=011.0_n=0400' + '-norm_cdf.npy'))
#     gn_cdf = np.load(os.path.join(s.d, 'm=011.0_n=0400', 'm=011.0_n=0400' + '-gn_cdf.npy'))
#     x = np.zeros_like(ln_x, dtype=object)
#     for idx, i in enumerate(ln_x):
#         x[idx] = mp.exp(i)
#     print x
#     np.save(os.path.join(s.d, 'm=011.0_n=0400', 'm=011.0_n=0400' + '-x.npy'), x)
#     print ln_x.shape, x.shape, norm_cdf.shape, gn_cdf.shape

#     ln_x = np.load(os.path.join(s.d, 'm=014.0_n=0300', 'm=014.0_n=0300' + '-ln_x.npy'))
#     x = np.load(os.path.join(s.d, 'm=014.0_n=0300', 'm=014.0_n=0300' + '-x.npy'))
#     norm_cdf = np.load(os.path.join(s.d, 'm=014.0_n=0300', 'm=014.0_n=0300' + '-norm_cdf.npy'))
#     gn_cdf = np.load(os.path.join(s.d, 'm=014.0_n=0300', 'm=014.0_n=0300' + '-gn_cdf.npy'))
#     x = np.zeros_like(ln_x, dtype=object)
#     for idx, i in enumerate(ln_x):
#         x[idx] = mp.exp(i)
#     print x
#     np.save(os.path.join(s.d, 'm=014.0_n=0300', 'm=014.0_n=0300' + '-x.npy'), x)
#     print ln_x.shape, x.shape, norm_cdf.shape, gn_cdf.shape

    from scratch.recursion.mp_settings import MPF_ONE, MPF_TWO, MPF_THREE
    from scratch.recursion.fn_lib import  weib_cdf_vect, norm_cdf_vect, weibul_plot_vect, differentiate, sn_mp, weibl_cdf_vect
    shape = mp.mpf(14.0)
    scale = MPF_ONE
#     ln_x = np.load(os.path.join(s.d, 'm=014.0_n=0400', 'm=014.0_n=0400' + '-ln_x.npy'))
#     x = np.load(os.path.join(s.d, 'm=014.0_n=0400', 'm=014.0_n=0400' + '-x.npy'))
#     weibr_wp = np.load(os.path.join(s.d, 'm=014.0_n=0400', 'm=014.0_n=0400' + '-weibr_wp.npy'))
#     norm_wp = np.load(os.path.join(s.d, 'm=014.0_n=0400', 'm=014.0_n=0400' + '-norm_wp.npy'))
#     gn_wp = np.load(os.path.join(s.d, 'm=014.0_n=0400', 'm=014.0_n=0400' + '-gn_wp.npy'))
#     n_fil = mp.mpf('400')
#
#     c = mp.exp(-MPF_ONE / shape)
#     std_est = (mp.power(shape, -MPF_ONE / shape) *
#                scale * mp.sqrt(c * (MPF_ONE - c)) / mp.sqrt(n_fil))
#     mean_est = (mp.power(shape , -MPF_ONE / shape) * scale * c +
#                 mp.power(n_fil, -MPF_TWO / MPF_THREE) * scale *
#                 mp.power(shape , -(MPF_ONE / shape + MPF_ONE / MPF_THREE)) *
#                 mp.exp(-MPF_ONE / (MPF_THREE * shape)) * mp.mpf('0.996'))
#     norm_cdf = norm_cdf_vect(x, mean_est, std_est)
#
#     print ln_x.shape, weibr_wp.shape, norm_wp.shape, gn_wp.shape
#     # np.save(os.path.join(s.d, 'm=014.0_n=0400', 'm=014.0_n=0400' + '-norm_wp.npy'), weibul_plot_vect(norm_cdf))
#
#
#     ln_x = np.load(os.path.join(s.d, 'm=012.0_n=0500', 'm=012.0_n=0500' + '-ln_x.npy'))
#     x = np.load(os.path.join(s.d, 'm=012.0_n=0500', 'm=012.0_n=0500' + '-x.npy'))
#     weibr_cdf = np.load(os.path.join(s.d, 'm=012.0_n=0500', 'm=012.0_n=0500' + '-weibr_cdf.npy'))
#     norm_wp = np.load(os.path.join(s.d, 'm=012.0_n=0500', 'm=012.0_n=0500' + '-norm_wp.npy'))
#     gn_wp = np.load(os.path.join(s.d, 'm=012.0_n=0500', 'm=012.0_n=0500' + '-gn_wp.npy'))
#     n_fil = mp.mpf('0500')
#
#     print ln_x.shape, weibr_cdf.shape, norm_wp.shape, gn_wp.shape
#     scale_r = scale / mp.power(n_fil, MPF_ONE / shape)
#     weibr_cdf = weib_cdf_vect(x, shape, scale_r)
#     np.save(os.path.join(s.d, 'm=012.0_n=0500', 'm=012.0_n=0500' + '-weibr_cdf.npy'), weibr_cdf)

    # mask = loadplot_data(os.path.join(s.d, s.name))
    # plt.show()
    #
    # for res in res_lst:
    #    data = np.load(os.path.join(s.d, s.name + '-%s.npy' % res))
    #    data = data[mask]
    #    np.save(os.path.join(s.d, s.name + '-%s.npy' % res), data)
    #
    # shutil.move(os.path.join(s.d), os.path.join(os.path.split(s.d)[0] + '_checked', s.name))

    # clear inf values
#     data = np.load(os.path.join(s.d, 'n=0033_m=20.0', 'n=0033_m=20.0' + '-dn.npy'))
#     print data
#
#     subdir_lst, path_lst = load_subdir_lists(s.d)
#     for sub in subdir_lst:
#         # for res in res_lst:
#         data = np.load(os.path.join(s.d, sub, sub + '-dn.npy'))
#         mask = (data == -mp.nan) + (data == mp.nan)
#         mp.mp.dps = 10
#         print data
    #        if np.sum(mask) > 0:
    #            mask = ~mask
    #            for res in res_lst:
    #                data = np.load(os.path.join(s.d, sub, sub + '-%s.npy' % res))
    #                data = data[mask]
    #                np.save(os.path.join(s.d, sub, sub + '-%s.npy' % res), data)
    #            print sub

    # delete last value in diff arrays
    # res_lst = ['gn_diff', 'ln_x_diff', 'norm_diff', 'x_diff']
    # subdir_lst, path_lst = load_subdir_lists(s.d)
    # for sub in subdir_lst:
    #    for res in res_lst:
    #        data = np.load(os.path.join(s.d, sub, sub + '-%s.npy' % res))
    #        np.save(os.path.join(s.d, sub, sub + '-%s.npy' % res), data[:-1])

    print 'Finished!'
