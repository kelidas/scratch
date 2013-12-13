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

res_num = []
x_num = []
def Gn(x, scale, shape, n):
    rv = weibull_min(shape, scale=scale)
    cdf = rv.cdf(x)
    x_num.append(x)
    if n < 1:
        return 1.
    elif n == 1.:
        res_num.append(cdf)
        return cdf
    cdf_k = 1.
    res = 0.
    for k in range(1, int(n)):
        cdf_k *= cdf
        komb = comb(n, k)
        if k % 2 == 0.:
            komb = -komb
        res_1 = komb * cdf_k * Gn((n / (n - k)) * x, scale, shape, n - k)
        res += res_1
        res_num.append(res_1)

    cdf_k *= cdf
    if n % 2 == 0.:
        res_num.append(-cdf_k)
        res -= cdf_k
    else:
        res_num.append(cdf_k)
        res += cdf_k

    return res

x_par = []
def gn_mp(x_val, scale, shape, n, x_rat=1):
    global x_arr
    global param_arr
    rv = weibull_min(shape, scale=scale)
    cdf = rv.cdf(x_val)
    cdf_k = 1.
    res = 0.
    for k in range(1, int(n) + 1):
        if x_val in x_arr and param_arr[n - 1, k - 1, np.argwhere(x_arr == x_val)] != 0:
            res_p = param_arr[n - 1, k - 1, np.argwhere(x_arr == x_val)[0][0]]
        else:
            cdf_k *= cdf
            komb = comb(n, k)
            if k == n:
                gn = (-1) ** (k + 1) * komb * cdf_k * 1
            else:
                gn = (-1) ** (k + 1) * komb * cdf_k * gn_mp((n / (n - k)) * x_val, scale, shape, n - k, s.Rational(n, n - k) * x_rat)
                # print 'n =', n, 'k =', k, 'rat =', x_rat
                x_par.append(x_rat)
            res_p = gn
            if x_val not in x_arr:
                x_arr = np.append(x_arr, x_val)
            param_arr[n - 1, k - 1, np.argwhere(x_arr == x_val)[0][0]] = res_p
        # print res_p, ' + ',
        res += res_p

    return res


if __name__ == '__main__':
    #===============================================================================
    # Settings
    #===============================================================================
    shape = 6.
    scale = 1.
    n = 3.

    param_arr = np.zeros((n, n, 1000), dtype=np.float64)
    x_arr = np.array([], dtype=np.float64)


    rv = weibull_min(shape, scale=scale)

    #===============================================================================
    # Testing -- one x
    #===============================================================================
    xx = -0.3
    xx = np.exp(xx)
    xx = .8
    #----- Original implementation
    start = sysclock()
    gn = Gn(xx, scale, shape, n)
    print 'Gn time =', sysclock() - start
    start = sysclock()
    #----- Modified implementation
    recursion_gn_mp = gn_mp(xx, scale, shape, n)
    print 'gn_mp time =', sysclock() - start
    print 'Results (orig, modif, diff)', gn, ',', recursion_gn_mp, gn - recursion_gn_mp
    # print 'Parameter array', param_arr
    print recursion_gn_mp

    print 'count of ', len(res_num)
    u, indices = np.unique(res_num, return_inverse=True)
    print 'number of unique values', len(u)
    print 'number of x', len(x_num)
    u, indices = np.unique(x_num, return_inverse=True)
    print 'number of unique values x', len(u)
    print x_par
    print np.unique(np.array(x_par))
    # print 'pocet vicenasobnych', np.sum(np.bincount(indices) > 1)
    # print 'jedinecne hodnoty', u
    # print np.bincount(indices)

    exit()
    #===============================================================================
    # Testing and plotting - array
    #===============================================================================
    lnxe = 0.03
    lnxb = 1 / 96 * shape - 4.0
    xx = np.arange(lnxb, 1., (lnxe - lnxb) / 500.)
    # xx = linspace(-4, 1., 20)
    xx = np.exp(xx)
    recursion_gn_mp = np.zeros_like(xx)

    start = sysclock()
    for idx, x_v in enumerate(xx):
        param_arr = np.zeros((n, n, 1000), dtype=np.float64)
        x_arr = np.array([], dtype=np.float64)
        recursion_gn_mp[idx] = gn_mp(x_v, scale, shape, n)
    print 'gn_mp time =', sysclock() - start

    # gn = Gn(xx, scale, shape, n)

    cdf = rv.cdf(xx)
    x1 = log(xx)
    gn3 = np.piecewise(recursion_gn_mp,
                [recursion_gn_mp <= 10 ** (-12), recursion_gn_mp > 10 ** (-12)],
                [lambda recursion_gn_mp: log(recursion_gn_mp), lambda recursion_gn_mp: log(-log(1 - recursion_gn_mp)) ])
    gn1 = log(-log(1 - cdf))
    # gn2 = log(-log(1 - gn))
    # gn3 = log(-log(1 - recursion_gn_mp))
    print gn3

    # plt.plot(x1, gn1, 'b-x')
    # plt.plot(x1, gn2, 'r-x')
    plt.plot(x1, gn3, 'g-x')
    plt.show()

    data = np.vstack((xx.T, x1.T, recursion_gn_mp.T, gn3.T)).T
    np.savetxt('n=%02i_m=%.3f_mod.txt' % (n, shape), data)



