'''
Created on Mar 2, 2012

@author: kelidas
'''

from traits.api import implements, Str
from scipy.special import erf
from stats.spirrid import SPIRRID, Heaviside, RV, RF, IRF
from stats.spirrid.extras import SPIRRIDLAB
import math
import numpy as np
from scipy.stats import norm
import pylab as p
from compound_lab import rms_error, max_error, lognormal_pdf, chi_error, lognormal_cdf, beta_par, BETA


#===========================================================================
# Response function
#===========================================================================
class BasicPDF(RF):
    ur'''
Basic probability density function
    '''
    implements(IRF)

    title = Str('Basic pdf')

    def __call__(self, x, mu, cov):
        ''' Basic probability density function '''
        return norm(mu, mu * cov).pdf(x)

    cython_code = '''
            '''

    c_code = '''
            '''

def run():

    m_mu, std_mu = 3., 0.68
    m_cov, std_cov = 0.18, 0.067

    # discretize the control variable (x-axis)
    x_arr = np.linspace(0, 6.0, 1000)[1:]

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q = BasicPDF(),
                e_arr = x_arr,
                n_int = 100,
                tvars = dict(mu = RV('norm', m_mu, std_mu), #RV('beta', m_cov, std_cov),#BETA('beta', mu = m_mu, sig = std_mu, a = a, b = b),
                             cov = RV('norm', m_cov, std_cov)
                             ),
                sampling_type = 'TGrid',
                codegen_type = 'numpy',
                )

    #===========================================================================
    # Calculate
    #===========================================================================
    # calculate compounded distribution values
    cpd_pdf = s.mu_q_arr
    cpd_cdf = np.cumsum(cpd_pdf) * np.diff(x_arr)[0]

    # calculate first raw moment
    raw_1 = np.trapz(cpd_pdf * x_arr, x_arr)

    # calculate second raw moment
    raw_2 = np.trapz(cpd_pdf * x_arr ** 2, x_arr)
    std = np.sqrt(raw_2 - raw_1 ** 2)

    # calculate values of lognormal distrib
    lognorm_pdf = lognormal_pdf(x_arr, raw_1, std)
    lognorm_cdf = lognormal_cdf(x_arr, raw_1, std)

    # calculate error
    rms_err = rms_error(lognorm_pdf, cpd_pdf)
    max_err = max_error(lognorm_pdf, cpd_pdf)
    chi_err = chi_error(lognorm_pdf, cpd_pdf)

    # generate samples
    samples = s.sampling.get_samples(20)
    sample_args = [ sam[:, np.newaxis] for sam in samples]
    q_arr = s.q(x_arr[None, :], *sample_args)

    #===========================================================================
    # Print
    #===========================================================================

    print 'check unity\t', np.trapz(cpd_pdf, x_arr)
    print 'mean\t\t', raw_1
    print 'std\t\t', std
    print 'rms error\t', rms_err
    print 'max error\t', max_err
    print 'chi error\t', chi_err

    #===========================================================================
    # Plot
    #===========================================================================
    p.figure()
    # plot samples
    #p.plot(x_arr, q_arr.T, color = 'gray')
    # plot compounded distribution
    p.plot(x_arr, cpd_pdf, 'b-')
    # plot lognormal distribution, method of moments
    p.plot(x_arr, lognorm_pdf, color = 'red', linewidth = 2)
    data = np.loadtxt('maple_cpd.txt', delimiter = ',')
    p.plot(data[:, 0], data[:, 1], color = 'violet')

    p.figure()
    p.plot(x_arr, cpd_cdf, 'b-')
    # plot lognormal CDF, method of moments
    p.plot(x_arr, lognorm_cdf, color = 'red', linewidth = 2)

    p.show()





if __name__ == '__main__':
    run()


