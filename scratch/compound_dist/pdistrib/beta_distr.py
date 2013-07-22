'''
Created on Mar 3, 2012

@author: kelidas
'''
import math
import warnings
from copy import copy

from scipy import special
from scipy import optimize
from scipy import integrate
from scipy.special import gammaln as gamln

import inspect
from numpy import alltrue, where, arange, putmask, \
     ravel, take, ones, sum, shape, product, repeat, reshape, \
     zeros, floor, logical_and, log, sqrt, exp, arctanh, tan, sin, arcsin, \
     arctan, tanh, ndarray, cos, cosh, sinh, newaxis, array, log1p, expm1
from numpy import atleast_1d, polyval, ceil, place, extract, \
     any, argsort, argmax, vectorize, r_, asarray, nan, inf, pi, isinf, \
     power, NINF, empty
import numpy
import numpy as np
import numpy.random as mtrand
from numpy import flatnonzero as nonzero
from scipy.stats.distributions import rv_continuous, _skew, _kurtosis
from traits.api import implements, Str, Property
import os

FILE_DIR = os.path.dirname(__file__)

class beta_gen(rv_continuous):
    def _rvs(self):
        a, b = np.loadtxt(os.path.join(FILE_DIR, 'distr_par.txt'), delimiter = ',')
        return mtrand.beta(a, b, self._size)
    def _pdf(self, x):
        a, b = np.loadtxt(os.path.join(FILE_DIR, 'distr_par.txt'), delimiter = ',')
        Px = (1.0 - x) ** (b - 1.0) * x ** (a - 1.0)
        Px /= special.beta(a, b)
        return Px
    def _logpdf(self, x):
        a, b = np.loadtxt(os.path.join(FILE_DIR, 'distr_par.txt'), delimiter = ',')
        lPx = (b - 1.0) * log(1.0 - x) + (a - 1.0) * log(x)
        lPx -= log(special.beta(a, b))
        return lPx
    def _cdf(self, x):
        a, b = np.loadtxt(os.path.join(FILE_DIR, 'distr_par.txt'), delimiter = ',')
        return special.btdtr(a, b, x)
    def _ppf(self, q):
        a, b = np.loadtxt(os.path.join(FILE_DIR, 'distr_par.txt'), delimiter = ',')
        return special.btdtri(a, b, q)
    def _stats(self):
        a, b = np.loadtxt(os.path.join(FILE_DIR, 'distr_par.txt'), delimiter = ',')
        mn = a * 1.0 / (a + b)
        var = (a * b * 1.0) / (a + b + 1.0) / (a + b) ** 2.0
        g1 = 2.0 * (b - a) * sqrt((1.0 + a + b) / (a * b)) / (2 + a + b)
        g2 = 6.0 * (a ** 3 + a ** 2 * (1 - 2 * b) + b ** 2 * (1 + b) - 2 * a * b * (2 + b))
        g2 /= a * b * (a + b + 2) * (a + b + 3)
        return mn, var, g1, g2
    def _fitstart(self, data):
        g1 = _skew(data)
        g2 = _kurtosis(data)
        def func(x):
            a, b = x
            sk = 2 * (b - a) * sqrt(a + b + 1) / (a + b + 2) / sqrt(a * b)
            ku = a ** 3 - a ** 2 * (2 * b - 1) + b ** 2 * (b + 1) - 2 * a * b * (b + 2)
            ku /= a * b * (a + b + 2) * (a + b + 3)
            ku *= 6
            return [sk - g1, ku - g2]
        a, b = optimize.fsolve(func, (1.0, 1.0))
        return super(beta_gen, self)._fitstart(data, args = (a, b))
    def fit(self, data, *args, **kwds):
        floc = kwds.get('floc', None)
        fscale = kwds.get('fscale', None)
        if floc is not None and fscale is not None:
            # special case
            data = (ravel(data) - floc) / fscale
            xbar = data.mean()
            v = data.var(ddof = 0)
            fac = xbar * (1 - xbar) / v - 1
            a = xbar * fac
            b = (1 - xbar) * fac
            return a, b, floc, fscale
        else: # do general fit
            return super(beta_gen, self).fit(data, *args, **kwds)
beta_distr = beta_gen(a = 0, b = 1.0, name = 'beta', shapes = 'a, b', extradoc = """

Beta distribution

beta.pdf(x, a, b) = gamma(a+b)/(gamma(a)*gamma(b)) * x**(a-1) * (1-x)**(b-1)
for 0 < x < 1, a, b > 0.
""")

if __name__ == '__main__':
    rv = beta_distr()
    x = np.linspace(0, 10, 1000)
    import pylab as p
    p.plot(x, rv.pdf(x))
    p.show()
