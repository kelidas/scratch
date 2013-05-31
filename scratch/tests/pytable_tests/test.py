import numpy as np
import mpmath as mp



data = np.array([1, 2, 3], dtype='mp.mpf')
np.save('test.npy', data)
data = np.load('test.npy', mmap_mode='r')
print data


data = np.memmap('data.dat', dtype=object, mode='r')
print 'fadsfsafA', data
