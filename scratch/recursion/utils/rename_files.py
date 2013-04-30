import os
from fnmatch import fnmatch
import re

from scratch.recursion.database_prep import DATABASE_DIR

# root = DATABASE_DIR
# pattern = r'*.npy'
#
# name_lst = []
# path_lst = []
# for path, subdirs, files in os.walk(root):
#     for name in files:
#         if fnmatch(name, pattern):
#             name_lst.append(name)
#             path_lst.append(path)

# change number formatting in names
# for name, path in zip(name_lst, path_lst):
#     m = re.findall(r'n=(\d+)_m=(\d+.\d+)(.*)', name)
#     try:
#         new_name = 'n={0:04d}_m={1:.1f}-{2}'.format(int(m[0][0]), float(m[0][1]), m[0][2])
#         #print new_name
#         #print name
#         #print m
#         os.rename(os.path.join(path, name), os.path.join(path, new_name))
#     except:
#         pass


# RENAME SHAPE DIRECTORIES
# root = DATABASE_DIR
# print os.listdir(DATABASE_DIR)
# for subdir in os.listdir(DATABASE_DIR):
#     try:
#         m = re.findall(r'm=(\d+.\d+)', subdir)
#         new_name = 'm={0:05.1f}'.format(float(m[0]))
#         print new_name
#         print subdir
#         # os.rename(os.path.join(DATABASE_DIR, subdir), os.path.join(DATABASE_DIR, new_name))
#     except:
#         pass




# Rename gn_cdf...
root = DATABASE_DIR
pattern = r'*'

name_lst = []
path_lst = []
for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            name_lst.append(name)
            path_lst.append(path)

for name, path in zip(name_lst, path_lst):
    try:
        m = re.findall(r'n=(\d+)_m=(\d+.\d+)(.*)', name)
        if m[0][-1] == '-gn_cdf':
            new_name = 'n={0:04d}_m={1:.1f}-{2}'.format(int(m[0][0]), float(m[0][1]), 'gn_cdf.npy')
            print new_name
            print name
            print m
            os.rename(os.path.join(path, name), os.path.join(path, new_name))
    except:
        pass

print 'Finished!'
