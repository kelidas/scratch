from scratch.recursion.temp.recursion import Gn
from scratch.recursion.recursion_mp import gn_mp
import numpy as np
import mpmath as mp
import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
import matplotlib.pyplot as plt

shape = 6.0
scale = 1.0
n_fil = 3.0
lnx = -0.5
x = .6  # np.exp(lnx)

# t_mp_lst = []
#
# n_lst = np.arange(5., 200, 10)
# for n in n_lst:
#     t_mp = sysclock()
#     g_mp = gn_mp(x, scale, shape, n, False)
#     t_mp = sysclock() - t_mp
#
#     t_mp_lst.append(t_mp)
#     print n, g_mp
#
# t_mp_lst = np.array(t_mp_lst)
# np.save('tmp_10.npy', np.vstack((n_lst, t_mp_lst)).T)
#
# plt.plot(n_lst, t_mp_lst)



# OLD version of recursion (naive)
# t_lst = []
# n_lst = np.arange(3., 19)
# for n in n_lst:
#     t = sysclock()
#     g = Gn(x, scale, shape, n)
#     t = (sysclock() - t)
#
#     t_lst.append(t)
#     print n, g
#
# t_lst = np.array(t_lst)
# np.save('t_old.npy', np.vstack((n_lst, t_lst)).T)
#
# plt.plot(n_lst, t_lst)




data_old = np.load('t_old.npy')
data_100 = np.load('tmp_100.npy')
data_1000 = np.load('tmp_1000.npy')
data_10000 = np.load('tmp_10000.npy')

plt.plot(data_old[:, 0], data_old[:, 1], label='old')
plt.plot(data_100[:, 0], data_100[:, 1], label='100')
plt.plot(data_1000[:, 0], data_1000[:, 1], label='1000')
plt.plot(data_10000[:, 0], data_10000[:, 1], label='10000')
plt.legend(loc='best')

plt.show()











