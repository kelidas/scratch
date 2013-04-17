import numpy as np
import os
from database_prep import res_lst
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
from database_prep import DATABASE_DIR

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
    s = Selector(d=DATABASE_DIR)
    #s.configure_traits()

    #mask = loadplot_data(os.path.join(s.d, s.name))
    #plt.show()
    #
    #for res in res_lst:
    #    data = np.load(os.path.join(s.d, s.name + '-%s.npy' % res))
    #    data = data[mask]
    #    np.save(os.path.join(s.d, s.name + '-%s.npy' % res), data)
    #
    #shutil.move(os.path.join(s.d), os.path.join(os.path.split(s.d)[0] + '_checked', s.name))

    # clear inf values
    #subdir_lst, path_lst = load_subdir_lists(s.d)
    #for sub in subdir_lst:
    #    for res in res_lst:
    #        data = np.load(os.path.join(s.d, sub, sub + '-%s.npy' % res))
    #        mask = (data == -mp.inf) + (data == mp.inf)
    #        if np.sum(mask) > 0:
    #            mask = ~mask
    #            for res in res_lst:
    #                data = np.load(os.path.join(s.d, sub, sub + '-%s.npy' % res))
    #                data = data[mask]
    #                np.save(os.path.join(s.d, sub, sub + '-%s.npy' % res), data)
    #            print sub

    # delete last value in diff arrays
    #res_lst = ['gn_diff', 'ln_x_diff', 'norm_diff', 'x_diff']
    #subdir_lst, path_lst = load_subdir_lists(s.d)
    #for sub in subdir_lst:
    #    for res in res_lst:
    #        data = np.load(os.path.join(s.d, sub, sub + '-%s.npy' % res))
    #        np.save(os.path.join(s.d, sub, sub + '-%s.npy' % res), data[:-1])

    print 'Finished!'
