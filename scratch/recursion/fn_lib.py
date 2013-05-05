import mpmath as mp
import numpy as np
import platform
from scipy.optimize import leastsq
import inspect
import time
if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock
from mp_settings import MPF_ONE, MPF_TWO

def weib_cdf(x, shape, scale):
    '''
    Cumulative distribution function of Weibull distribution with two
    parameters (shape and scale).
    '''
    return MPF_ONE - mp.exp(-(x / scale) ** shape)

weib_cdf_vect = np.frompyfunc(weib_cdf, 3, 1)

def norm_cdf(x, mean, std):
    '''
    Cumulative distribution function of Normal distribution with two
    parameters (mean and standard deviation).
    '''
    return (MPF_ONE + mp.erf((x - mean) / mp.sqrt(MPF_TWO * std ** 2))) / MPF_TWO

norm_cdf_vect = np.frompyfunc(norm_cdf, 3, 1)

def weibl_cdf(x, sn, shape, n):
    '''
    Return values of the left asymptote for cumulative distribution function of
    bundle strength.
    '''
    return (x / sn) ** (shape * n)

weibl_cdf_vect = np.frompyfunc(weibl_cdf, 4, 1)

def weibul_plot(g):
    '''
    Transform data for Weibull plot
    '''
    return mp.log(-mp.log(MPF_ONE - g)).real

weibul_plot_vect = np.frompyfunc(weibul_plot, 1, 1)

def sn_mp(dn, scale, shape, n):
    '''Scale parameter for the left asymptote of G_n
    '''
    return scale / dn ** (MPF_ONE / (n * shape))

def differentiate(x, y):
    '''Calculate the derivatives for given arrays x and y
    '''
    return np.diff(y) / np.diff(x)

def dk_approx(k, scale, shape, gn_wp, ln_x):
    '''Calculate approximate position of the tangent
    '''
    if isinstance(scale, mp.mpf) == False:
        scale = mp.mpf('%s' % scale)
    if isinstance(shape, mp.mpf) == False:
        shape = mp.mpf('%s' % shape)
    if isinstance(k, mp.mpf) == False:
        k = mp.mpf('%s' % k)
    b_approx = 0
    c_approx = 100

    import time
    bb = gn_wp - shape * k / scale * ln_x
    ln_x = shape * k / scale * ln_x
    for b in bb:
        y = ln_x + b
        counter = np.sum(y < gn_wp)
        if counter < c_approx:
            c_approx = counter
            counter = 0
            b_approx = b
        else:
            counter = 0
    return mp.exp(b_approx)

def f_weib(x, a, b, c):
    '''CDF of the Weibull distribution reflected across the axis y.
    '''
    return 1 - np.exp(-(-(x - c) / a) ** b)

def f_gumb(x, a, b):
    '''CDF of the Gumbel distribution reflected across the axis y.
    '''
    return np.exp(-np.exp(-(-x - a) / b))

def f_gev(x, a, b, c):
    '''CDF of the Generalized extreme value distribution reflected across the axis y.
    '''
    return np.exp(-(1 + a * ((-x - b) / c)) ** (-1.0 / a))

def fit_data_leastsq(f, x, y, p0=None):
    '''Fitting data using scipy leastsq function.
    '''
    if p0 == None:
        n_arg = len(inspect.getargspec(f).args)
        p0 = np.ones(n_arg - 1)

    def residuals(p, y, x):
        err = y - f(x, *p)
        return err

    plsq = leastsq(residuals, p0, args=(y, x))
    print 'plsq', plsq
    return f(x, *plsq[0])






