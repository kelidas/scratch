# import neurolab as nl
# # Create network
# net = nl.net.newff([[-1, 1]], [5, 1])
# # Default train function (train_gdx)
# print net.trainf
# # Change train function
# net.trainf = nl.train.train_gdm
# # Change init function
# for l in net.layers:
#     l.initf = nl.init.InitRand([-2., 2.], 'wb')
# # new inicialized
# net.init()
# # Change error function
# net.errorf = nl.error.MSE()
# # Change weight of input layer
# net.layers[0].np['w'][:] = 0.0
# print net.layers[0].np['w']
# # Change bias of input layer
# net.layers[0].np['b'][:] = 1.0
# print net.layers[0].np['b']
#
# # Save network in file
# net.save('test.net')
# # Load network
# net = nl.load('test.net')

import neurolab as nl
import numpy as np

# Create train samples
x = np.linspace(-7, 7, 20)
y = np.sin(x) * 0.5

size = len(x)

inp = x.reshape(size, 1)
tar = y.reshape(size, 1)

# Create network with 2 layers and random initialized
net = nl.net.newff([[-7, 7]], [5, 1],
                   [nl.trans.TanSig(), nl.trans.PureLin()]
                   )

# Train network
#net.trainf = nl.train.train_rprop
error = net.train(inp, tar, epochs=500, show=100, goal=0.02)

# Simulate network
out = net.sim(inp)

# Plot result
import pylab as pl
pl.subplot(211)
pl.plot(error)
pl.xlabel('Epoch number')
pl.ylabel('error (default SSE)')

x2 = np.linspace(-6.0, 6.0, 150)
y2 = net.sim(x2.reshape(x2.size, 1)).reshape(x2.size)

y3 = out.reshape(size)

pl.subplot(212)
pl.plot(x2, y2, '-', x, y, '.', x, y3, 'p')
pl.legend(['train target', 'net output'])
pl.show()
