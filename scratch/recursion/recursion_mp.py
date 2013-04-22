# -------------------------------------------------------------------------------
#
# Copyright (c) 2013
# Author: Vaclav Sadilek
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in the top directory "licence.txt" and may be
# redistributed only under the conditions described in the aforementioned
# license.
#
# -------------------------------------------------------------------------------

import mpmath as mp
import numpy as np
import platform
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from fn_lib import weib_cdf
# import sys
# sys.setrecursionlimit(10000)

from mp_settings import MPF_ZERO, MPF_ONE
from binomial_tab import get_binom_tab

__all__ = ['gn_mp', 'gn_mp_vect', 'dn_mp']

binom_tab = get_binom_tab()

# TODO: make recursion-less alternative of gn_mp - using loops for ?
def gn_mp(x, scale, shape, n, timeit=False):
    '''
    Return value of cumulative distribution function of a bundle strength
    considering Weibull distribution of fibers.

    Parameters
    ----------
    x : mpf (float)
        Bundle strength
    scale : mpf (float)
        Scale parameter of Weibull distribution
    shape : mpf (float)
        Shape parameter of Weibull distribution
    n : mpf (int)
        Number of filaments
    timeit : bool, optional
        Execution time of one x. Default: False.

    Returns
    -------
    out : mpf
        Cumulative distribution function value for required strength x

    Examples
    --------
    >>> mp.mp.dps = 30
    >>> shape = mp.mpf('6.')
    >>> scale = mp.mpf('1.')
    >>> n_fil = mp.mpf('10')
    >>> x = mp.exp(mp.mpf('-1'))
    >>> gn_mp(x, scale, shape, n_fil, timeit=False)
    mpf('0.000000329859130502740500994574682994377')
    '''
    global binom_tab
    gn_arr = np.zeros((n, n), dtype=object)
    gn_arr.fill(None)
    cdf_arr = np.zeros(n, dtype=object)
    cdf_arr.fill(None)
    x_arr = np.zeros(n, dtype=object)
    for i in range(1, n):
        x_arr[n - i] = mp.fraction(n, n - i) * x
    def recursion_gn_mp(x_val, scale, shape, n):
        index_n = int(n) - 1
        res = MPF_ZERO
        cdf = cdf_arr[index_n]
        if cdf == None:
            cdf = weib_cdf(x_val, shape, scale)
            cdf_arr[index_n] = cdf
        for k in range(1, int(n) + 1):
            gn = gn_arr[index_n, k - 1]
            if gn == None:
                cdf_k = cdf ** k
                komb = binom_tab[index_n, k - 1]
                if k != n:
                    gn = komb * cdf_k * recursion_gn_mp(x_arr[index_n], scale,
                                                        shape, n - k)
                else:
                    gn = komb * cdf_k  # * G_0(x) (= 1.0)
                gn_arr[index_n, k - 1] = gn
            res += gn
        return res
    if timeit:
        start = sysclock()
    gn_m = recursion_gn_mp(x, scale, shape, n)
    if timeit:
        print 'gn_mp time (one x value) =', sysclock() - start
    return gn_m

gn_mp_vect = np.frompyfunc(gn_mp, 5, 1)

def dn_mp(scale, shape, n, timeit=False):
    '''
    Return value dn that is used for evaluation of the left asymptote of
    cumulative distribution function of a bundle strength.

    Parameters
    ----------
    scale : mpf (float)
        Scale parameter of Weibull distribution
    shape : mpf (float)
        Shape parameter of Weibull distribution
    n : mpf (int)
        Number of filaments
    timeit : bool, optional
        Execution time of one x_val. Default: False.

    Returns
    -------
    out : mpf
        Value of parameter dn

    Examples
    --------
    >>> mp.mp.dps = 30
    >>> shape = mp.mpf('6.')
    >>> scale = mp.mpf('1.')
    >>> n_fil = mp.mpf('10')
    >>> dn_mp(scale, shape, n_fil, timeit=False)
    mpf('244036475766801116896748171.011047')
    '''
    global binom_tab
    param_dn_arr = np.zeros((n, n), dtype=object)
    param_dn_arr.fill(None)
    def recursion_dn_mp(scale, shape, n):
        res = MPF_ONE
        if n != 1:
            index_n = int(n) - 1
            res = mp.mpf('-1') ** (n + MPF_ONE)
            for k in range(1, int(n)):
                dn = param_dn_arr[index_n, k - 1]
                if dn == None:
                    komb = binom_tab[index_n, k - 1]
                    # TODO: mp.fraction(n, (n - k))** (mp.mpf(n - k) could be precalculated in frac_tab as x_arr (in gn_mp) and than used as (frac_tab[] ** shape)
                    dn = (komb * mp.fraction(n, (n - k)) ** (shape * mp.mpf(n - k))
                          * recursion_dn_mp(scale, shape, n - k))
                    param_dn_arr[index_n, k - 1] = dn
                res += dn
        return res
    if timeit:
        start = sysclock()
    dn_m = recursion_dn_mp(scale, shape, n)
    if timeit:
        print 'dn_mp time =', sysclock() - start
    return dn_m

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    mp.mp.dps = 1000
    shape = mp.mpf('6.')
    scale = mp.mpf('1.')
    n_fil = mp.mpf('10')
    x1 = mp.exp(mp.mpf('-1'))

    recursion_gn_mp = gn_mp_vect(x1, scale, shape, n_fil, True)
    print 'Result of recursion_gn_mp for one x value =', recursion_gn_mp

    # TODO: computational time estimation
    t_est = 0
    for i in range(10):
        start = sysclock()
        gn_mp_vect(x1, scale, shape, mp.mpf('50'), False)
        t_est += sysclock() - start
    print 'time estimation', t_est / 10.



