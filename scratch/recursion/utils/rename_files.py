import os
from fnmatch import fnmatch
import re

root = r'.'
pattern = r'*.npy'

name_lst = []
path_lst = []
for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            name_lst.append(name)
            path_lst.append(path)

for name, path in zip(name_lst, path_lst):
    m = re.findall(r'n=(\d+)_m=(\d+.\d+)(.*)', name)
    try:
        new_name = 'n={0:04d}_m={1:.1f}-{2}'.format(int(m[0][0]), float(m[0][1]), m[0][2])
        #print new_name
        #print name
        #print m
        os.rename(os.path.join(path, name), os.path.join(path, new_name))
    except:
        pass


print 'Finished!'
