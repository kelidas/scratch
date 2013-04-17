'''
Created on Mar 2, 2012

@author: kelidas
'''
import numpy as np
from scipy.stats import lognorm, chisquare, norm, beta, ks_2samp
from scipy.optimize import fsolve
from stats.pdistrib.distribution import Distribution
from stats.spirrid import SPIRRID, Heaviside, RV, RF, IRF
from traits.api import HasTraits, Float, Int, Event, Array, Interface, \
    Tuple, Property, cached_property, Instance, Enum, on_trait_change, implements, Str
from stats.pdistrib.pdistrib import IPDistrib

def lognormal_pdf(x, mu, sig):
    '''
    Lognormal PDF
    '''
    cov = sig / mu
    zeta = np.sqrt(np.log(cov ** 2 + 1))
    lambd_ = np.log(mu) - 0.5 * zeta ** 2
    y = (np.log(x) - lambd_) / zeta
    return np.exp(-0.5 * y ** 2) / (x * zeta * np.sqrt(2 * np.pi))

def lognormal_cdf(x, mu, sig):
    cov = sig / mu
    zeta = np.sqrt(np.log(cov ** 2 + 1))
    lambd_ = np.log(mu) - 0.5 * zeta ** 2
    y = (np.log(x) - lambd_) / zeta
    return norm(0, 1).cdf(y)

def lognormal_2(x, mu, sig):
    rv = Distribution(lognorm)
    rv.variance = sig ** 2
    rv.mean = mu
    return lognorm(rv.shape, rv.loc, rv.scale).pdf(x)

def rms_error(y1, y2):
    '''
    y1 .. chceme dosahnout
    y2 .. pokus
    '''
    return np.sqrt(np.nansum((y2 - y1) ** 2) / len(y1)) / np.nanmax(y1)

def max_error(y1, y2):
    '''
    y1 .. chceme dosahnout
    y2 .. pokus
    '''
    return np.nanmax(np.abs(y1 - y2)) / np.nanmax(y1)

def chi_error(y1, y2):
    '''
    y1 .. chceme dosahnout
    y2 .. pokus
    '''
    return chisquare(y2, f_exp = y1)

def ks_error(y1, y2):
    '''
    y1 .. chceme dosahnout
    y2 .. pokus
    '''
    return ks_2samp(y1, y2)

def beta_pdf(x, mu, sig, a, b):
    s = (mu - a) / (b - a)
    e = (b - a) / sig
    q = s * s * e * e
    alpha = q * (1 - s) - s
    beta_ = q * (s - 2) + s * (1 + e * e) - 1
    print alpha, beta_
    return beta(alpha, beta_, loc = a, scale = (b - a)).pdf(x)

def beta_par(mu, sig, a, b):
    s = (mu - a) / (b - a)
    e = (b - a) / sig
    q = s * s * e * e
    alpha = q * (1 - s) - s
    beta_ = q * (s - 2) + s * (1 + e * e) - 1
    return alpha, beta_, a, b

def beta_cdf(x, mu, sig, a, b):
    s = (mu - a) / (b - a)
    e = (b - a) / sig
    q = s * s * e * e
    alpha = q * (1 - s) - s
    beta_ = q * (s - 2) + s * (1 + e * e) - 1
    return beta(alpha, beta_, loc = a, scale = (b - a)).cdf(x)

if __name__ == '__main__':
    x = np.linspace(0, 10, 1000)[1:]
    y = beta_pdf(x, 3.2126, 0.655, 0, 3.4)

    import pylab as p

    p.plot(x, y)
    p.show()
