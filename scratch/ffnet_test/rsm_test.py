import ffnet
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm, gumbel_r
import ctypes
import shutil


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

data_LHS = np.genfromtxt(os.path.join(
    '/home/kelidas/Downloads', '%dsim_RSM.txt' % n_sim), skip_header=1)
inp_LHS = data_LHS[:, :-1]
out_LHS = data_LHS[:, -1][:, np.newaxis]

net = ffnet.loadnet('ffnet_net.pkl')
res = net.call(inp_LHS)

print res
print res - out_LHS

n_MC = 1000000
x1_MC = x1.rvs(n_MC)
x2_MC = x2.rvs(n_MC)
x3_MC = x3.rvs(n_MC)
x4_MC = x4.rvs(n_MC)
rsm_MC = net.call(np.vstack((x1_MC, x2_MC, x3_MC, x4_MC)).T)
print rsm_MC
pf = np.sum(rsm_MC < 0) / float(n_MC)
rv = norm(0, 1)
beta = -rv.ppf(pf)
print pf, beta
print np.min(rsm_MC)
