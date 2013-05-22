from scratch.recursion.temp.recursion_mp_loop import Gn
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


# data_1000 = np.load('tmp_1000.npa')
# data_1000_n = data_1000[:, 0]
# data_1000_t = data_1000[:, 1]
#
#
# print data_1000_t.shape, data_1000_n.shape
# n_lst = np.arange(730, 1001, 10)
# for n in n_lst:
#     t_mp = sysclock()
#     g_mp = gn_mp(x, scale, shape, n, False)
#     t_mp = sysclock() - t_mp
#
#     data_1000_t = np.append(data_1000_t, np.array([t_mp]))
#     data_1000_n = np.append(data_1000_n, np.array([n]))
#     print n, g_mp
#     np.save('tmp_1000.npa', np.vstack((data_1000_n, data_1000_t)).T)
#
# plt.plot(data_1000_n, data_1000_t)
# plt.show()

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
# np.save('tmp_10.npa', np.vstack((n_lst, t_mp_lst)).T)
#
# plt.plot(n_lst, t_mp_lst)

# OLD version of recursion (naive)
# t_lst = []
# n_lst = np.arange(3., 18)
# for n in n_lst:
#     t = sysclock()
#     g = Gn(x, scale, shape, n)
#     t = (sysclock() - t)
#
#     t_lst.append(t)
#     print n, g
#
# t_lst = np.array(t_lst)
# np.save('t_old_mp_gmpy.npa', np.vstack((n_lst, t_lst)).T)
#
# plt.plot(n_lst, t_lst)


from scipy import stats

data_old = np.load('t_old.npa')
data_old_mp = np.load('t_old_mp.npa')
data_old_mp_gmpy = np.load('t_old_mp_gmpy.npa')
data_old_c = np.load('t_old_c.npa')
data_100 = np.load('tmp_100.npa')
data_1000 = np.load('tmp_1000.npa')
data_1000_gmpy = np.load('tmp_1000_gmpy.npa')
data_10000 = np.load('tmp_10000.npa')

print 'old'
slope, intercept, r_value, p_value, std_err = stats.linregress(data_old[:, 0], np.log(data_old[:, 1]))
print 'slope =', slope, ', intercept =', intercept
print 'coefficient of determination =', r_value ** 2
data_old_fit = np.exp(slope * data_old[:, 0] + intercept)

print '100'
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(data_100[:, 0]), np.log(data_100[:, 1]))
print 'slope =', slope, ', intercept =', intercept
print 'coefficient of determination =', r_value ** 2
data_100_fit = np.exp(slope * np.log(data_100[:, 0]) + intercept)

print '1000'
mask = data_1000[:, 0] >= 400
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(data_1000[:, 0])[mask], np.log(data_1000[:, 1])[mask])
print 'slope =', slope, ', intercept =', intercept
print 'coefficient of determination =', r_value ** 2
data_1000_fit = np.exp(slope * np.log(data_1000[:, 0]) + intercept)
# print np.sum(np.exp(slope * np.log(np.arange(730, 1001, 10)) + intercept)) / 3600.

print '10000'
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(data_1000[:, 0]), np.log(data_1000[:, 1]))
print 'slope =', slope, ', intercept =', intercept
print 'coefficient of determination =', r_value ** 2

plt.plot(data_old[:, 0], data_old[:, 1], label='old')
plt.plot(data_old_mp[:, 0], data_old_mp[:, 1], label='old_mp')
plt.plot(data_old_mp_gmpy[:, 0], data_old_mp_gmpy[:, 1], label='old_mp_gmpy')
plt.plot(data_old_c[:, 0], data_old_c[:, 1], label='old_c')
plt.plot(data_old[:, 0], data_old_fit, 'k--')

plt.plot(data_100[:, 0], data_100[:, 1], label='100')
# plt.plot(data_100[:, 0], data_100_fit, 'k--')

plt.plot(data_1000[:, 0], data_1000[:, 1], label='1000')
plt.plot(data_1000_gmpy[:, 0], data_1000_gmpy[:, 1], label='1000_gmpy')
plt.plot(data_1000[:, 0][mask], data_1000_fit[mask], 'k--')

plt.plot(data_10000[:, 0], data_10000[:, 1], label='10000')
# plt.plot(data_10000[:, 0], data_10000_fit, 'k--')
plt.legend(loc='best')

plt.show()











