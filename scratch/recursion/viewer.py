import matplotlib.pyplot as plt
import numpy as np
from traits.api import HasStrictTraits, Float, Property, cached_property, \
    Event, Array, Instance, Range, on_trait_change, Bool, Trait, DelegatesTo, \
    Constant, Directory, File, Str, Button, Int, List
from pyface.api import FileDialog, warning, confirm, ConfirmationDialog, YES
from traitsui.api import View, Item, Group, OKButton, CodeEditor, VGroup, HSplit
import os
from fnmatch import fnmatch
import mpmath as mp
from mp_settings import MPF_ONE


def load_subdir_lists(dir_name):
    name_lst = []
    path_lst = []
    for path, subdirs, files in os.walk(dir_name):
        for name in subdirs:
            name_lst.append(name)
            path_lst.append(path)
    return name_lst, path_lst

class Selector(HasStrictTraits):

    f = File()

    part_name = Str()
    @on_trait_change('f')
    def _part_name(self):
        self.part_name = self.f.split('-')[0]

    traits_view = View(
                    Item('f'),
                    title='File Selector',
                    id='select',
                    dock='tab',
                    resizable=True,
                    width=.5,
                    height=.5,
                    buttons=[OKButton])

def loadplot_data(part_name):
    sn = np.load(part_name + '-sn.npy')
    x = np.load(part_name + '-x.npy')
    x_diff = np.load(part_name + '-x_diff.npy')
    ln_x = np.load(part_name + '-ln_x.npy')
    ln_x_diff = np.load(part_name + '-ln_x_diff.npy')

    recursion_gn_mp = np.load(part_name + '-gn_cdf.npy')
    norm_cdf = np.load(part_name + '-norm_cdf.npy')
    weibr_cdf = np.load(part_name + '-weibr_cdf.npy')
    weibl_cdf = np.load(part_name + '-weibl_cdf.npy')

    gn_diff = np.load(part_name + '-gn_diff.npy')
    norm_diff = np.load(part_name + '-norm_diff.npy')

    gn_wp = np.load(part_name + '-gn_wp.npy')
    wp_norm = np.load(part_name + '-norm_wp.npy')
    weibr_wp = np.load(part_name + '-weibr_wp.npy')
    weibl_wp = np.load(part_name + '-weibl_wp.npy')

    plt.figure(0)
    plt.plot(ln_x, recursion_gn_mp, 'r-')
    plt.plot(ln_x, norm_cdf, 'b-')
    plt.plot(ln_x, weibr_cdf, 'g-')
    plt.plot(ln_x, weibl_cdf, 'g-')
#    y = (x / sn) ** (10 * 4)
#    y[y > 1] = 1
#    plt.plot(ln_x, y)

    plt.figure(1)
    plt.plot(ln_x_diff, gn_diff, 'r-')
    plt.plot(ln_x_diff, norm_diff, 'b-')

    plt.figure(2)
    plt.plot(ln_x, gn_wp, 'r-')
    plt.plot(ln_x, wp_norm, 'b-')
    plt.plot(ln_x, weibr_wp, 'g-')
    plt.plot(ln_x, weibl_wp, 'g-')
    plt.xlim(-4.0, 0.5)
    # plt.ylim(-2280.0, 7.0)

    def form3(x, pos):
        mp.mp.dps = 1000
        return '%s %%' % mp.nstr((MPF_ONE - mp.exp(-mp.exp(x))) * 100, 6)
    formatter = plt.FuncFormatter(form3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(formatter))



s = Selector()
s.configure_traits()


def plot_one():
    loadplot_data(s.part_name)

def plot_all_n():
    dirname = os.path.split(os.path.split(s.part_name)[0])[0]

    subdir_lst, path_lst = load_subdir_lists(dirname)

    for path, subdir in zip(path_lst, subdir_lst):
        loadplot_data(os.path.join(path, subdir, subdir))
        print subdir


plot_one()
# plot_all_n()

plt.show()
