from scipy.misc import comb
from numpy import linspace, exp, log, abs
import numpy as np
import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
import matplotlib.pyplot as plt
import mpmath as mp

mp.mp.dps = 500

def weibul_cdf(x, shape, scale):
    return 1. - mp.exp(-(x / scale) ** shape)

def gn_mp(x_val, scale, shape, n):
    global param_arr
    cdf = weibul_cdf(x_val, shape, scale)
    cdf_k = mp.mpf(1.)
    res = mp.mpf(0.)
    for k in range(1, int(n) + 1):
        test = (param_arr[:, 0] == x_val) * (param_arr[:, 1] == n) * (param_arr[:, 2] == k)
        if np.sum(test) == 1:
            res_p = param_arr[test][0, 3]
        else:
            cdf_k *= cdf
            komb = mp.binomial(n, k)
            if k == n:
                gn = (-1) ** (k + 1) * komb * cdf_k * 1
            else:
                gn = (-1) ** (k + 1) * komb * cdf_k * gn_mp((n / (n - k)) * x_val, scale, shape, n - k)
            res_p = gn
            if np.sum(test) == 0:
                param_arr = np.append(param_arr, [[x_val, n, k, res_p]], axis=0)
        #print res_p, ' + ',
        res += res_p
    return res


#===============================================================================
# Settings
#===============================================================================
shape = mp.mpf(100.)
scale = mp.mpf(1.)
n = mp.mpf(20.)

param_arr = np.array([[-2, -2, -2, -2]], dtype=object)


#===============================================================================
# Testing -- one x
#===============================================================================
xx = mp.mpf(-10)
xx = mp.exp(xx)

start = sysclock()
#----- Modified implementation
recursion_gn_mp = gn_mp(xx, scale, shape, n)
print 'gn_mp time =', sysclock() - start
print 'Results', recursion_gn_mp

