import numpy as np
import mpmath as mp
import tables

mp.mp.dps = 1000

data = np.load('test.npy')
#print data

filename = "test.hdf5"

h5file = tables.openFile(filename, mode="w", title="Test file")

filters = tables.Filters(complib='blosc', complevel=9)
ds = h5file.createVLArray(h5file.root, 'somename', tables.ObjectAtom(), filters=filters)
ds.append(data)


h5file.close()

data_map = np.memmap('data.dat', dtype=object, mode='w+', shape=data.shape)
data_map[:] = data[:]


np.savez_compressed('test.npz', data=data)
data = np.load('test.npz')
print data['data']


data = np.memmap('data.dat', dtype=object, mode='r')
print 'fadsfsafA', data
