import numpy as np
import os
from database_prep import res_lst

def load_subdir_lists(dir_name):
    name_lst = []
    path_lst = []
    for path, subdirs, files in os.walk(dir_name):
        for name in subdirs:
            name_lst.append(name)
            path_lst.append(path)
    return name_lst, path_lst

dirname = os.getcwd()
print dirname
subdir_lst, path_lst = load_subdir_lists(dirname)

for path, subdir in zip(path_lst, subdir_lst):
    for res in res_lst:
        arr = np.array([], dtype=object)
        for i in range(10):
            name = os.path.join(path, subdir, '%02i_%s-' % (i + 1, subdir))
            arr = np.hstack((arr, np.load(name + res + '.npy')))
        name = '%s-' % subdir
        np.save(os.path.join(path, subdir, name + res + '.npy'), arr)


