from scipy.misc import comb
from scipy.stats import weibull_min
from numpy import linspace, exp, log, abs
import numpy as np
import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
import matplotlib.pyplot as plt
import sympy as s
import mpmath as mp
from scratch.recursion import fn_lib
from scratch.recursion.binomial_tab import get_binom_tab


binom_tab = get_binom_tab()

def Gn(x, scale, shape, n):
    cdf = fn_lib.weib_cdf(x, shape, scale)
    if n < 1:
        return 1.
    elif n == 1.:
        return cdf
    cdf_k = mp.mpf("1.")
    res = mp.mpf("0.")
    for k in range(1, int(n)):
        cdf_k *= cdf
        komb = binom_tab[int(n) - 1, k - 1]  # comb(int(n), k)

        # komb = mp.mpf("%f" % komb)
        # if k % 2 == 0.:
        #    komb = -komb
        res_1 = komb * cdf_k * Gn((n / (n - mp.mpf(k))) * x, scale, shape, mp.mpf(n - k))
        res += res_1

    cdf_k *= cdf
    if n % 2 == 0.:
        res -= cdf_k
    else:
        res += cdf_k
    return res



if __name__ == '__main__':
    #===============================================================================
    # Settings
    #===============================================================================
    shape = mp.mpf("6.")
    scale = mp.mpf("1.")
    n = mp.mpf("15.")

    #===============================================================================
    # Testing -- one x
    #===============================================================================
    xx = mp.mpf(".5")
    #----- Original implementation
    start = sysclock()
    gn = Gn(xx, scale, shape, n)
    print 'Gn time =', sysclock() - start
    print gn
