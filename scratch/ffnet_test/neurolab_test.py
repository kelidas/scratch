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

import os
import neurolab as nl
import numpy as np
from sklearn.preprocessing import normalize
import pylab as pl
from scipy.stats import norm, lognorm, gumbel_r

# Create train samples
data_LHS = np.genfromtxt(os.path.join(
    '/home/kelidas/Downloads', '%dsim_RSM.txt' % 10), skip_header=1)
inp_LHS = data_LHS[:, :-1]
out_LHS = data_LHS[:, -1][:, np.newaxis]

inp_LHS = (inp_LHS - inp_LHS.min(axis=0)) / \
    (inp_LHS.max(axis=0) - inp_LHS.min(axis=0)) * 2 - 1
pl.plot(inp_LHS)
pl.show()
print inp_LHS.shape

x1 = inp_LHS[:, 0][:, np.newaxis]
x2 = inp_LHS[:, 1][:, np.newaxis]
x3 = inp_LHS[:, 2][:, np.newaxis]
x4 = inp_LHS[:, 3][:, np.newaxis]

y = out_LHS

size = len(x1)

inp = inp_LHS  # x.reshape(size, 1)
tar = y  # y.reshape(size, 1)

# Create network with 2 layers and random initialized
net = nl.net.newff([[x1.min(), x1.max()],
                    [x2.min(), x2.max()],
                    [x3.min(), x3.max()],
                    [x4.min(), x4.max()]],
                   [4, 1],
                   [nl.trans.TanSig(), nl.trans.PureLin()]
                   )

# Train network
net.trainf = nl.train.train_rprop
error = net.train(inp, tar, epochs=5000, show=100, goal=1e-20, lr=0.001)

# Simulate network
out = net.sim(inp)
print out - out_LHS

# Plot result

pl.subplot(211)
pl.plot(error)
pl.xlabel('Epoch number')
pl.ylabel('error (default SSE)')


#x2 = np.linspace(-6.0, 6.0, 150)
y2 = net.sim(inp)

#y3 = out.reshape(size)

pl.subplot(212)
pl.plot(x1, y, '-', x1, y2, '.')
pl.plot(x2, y, '-', x2, y2, '.')
pl.plot(x3, y, '-', x3, y2, '.')
pl.plot(x4, y, '-', x4, y2, '.')
pl.legend(['train target', 'net output'])
pl.show()

n_serie = 5  # 1, 2, 3, 4, 5
n_sim = 10  # 10, 20, 30, 40, 50, 60
n_MC = 1000000
n_cMC = 10
ann_struct = '4i-1l'
x1 = norm(0.002244, 4.488e-5)  # mean, std
# zeta, scale=e^lambda
x2 = lognorm(0.06991447685, loc=0, scale=np.exp(12.96291461))
# zeta, scale=e^lambda
x3 = lognorm(0.05994610505, loc=0, scale=np.exp(10.00207896))
x4 = gumbel_r(loc=0.03909989358, scale=0.001559393602)  # loc=Mode, scale=beta

n_MC = 1000000
x1_MC = x1.rvs(n_MC)
x2_MC = x2.rvs(n_MC)
x3_MC = x3.rvs(n_MC)
x4_MC = x4.rvs(n_MC)


data = np.vstack((x1_MC, x2_MC, x3_MC, x4_MC)).T
data = (data - data.min(axis=0)) / \
    (data.max(axis=0) - data.min(axis=0)) * 2 - 1

rsm_MC = net.sim(data)
print rsm_MC
pf = np.sum(rsm_MC < 0) / float(n_MC)
rv = norm(0, 1)
beta = -rv.ppf(pf)
print pf, beta
print np.min(rsm_MC)
