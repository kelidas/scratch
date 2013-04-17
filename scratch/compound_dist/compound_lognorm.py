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
from compound_lab import rms_error, max_error, lognormal, chi_error

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
        return lognormal(x, mu, mu * cov)#lognormal_2(x, mu, mu * cov)

    cython_code = '''
            '''

    c_code = '''
            '''

def run():

    m_mu, std_mu = 3., 0.68
    m_cov, std_cov = 0.18, 0.067

    # discretize the control variable (x-axis)
    x_arr = np.linspace(0, 10.0, 1000)[1:]

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q = BasicPDF(),
                e_arr = x_arr,
                n_int = 100,
                tvars = dict(mu = RV('norm', m_mu, std_mu),
                             cov = RV('norm', m_cov, std_cov)
                             ),
                sampling_type = 'TGrid',
                codegen_type = 'numpy',
                )

    #===========================================================================
    # Calculate
    #===========================================================================
    # calculate compounded distribution values
    y = s.mu_q_arr

    # calculate first raw moment
    raw_1 = np.trapz(y * x_arr, x_arr)

    # calculate second raw moment
    raw_2 = np.trapz(y * x_arr ** 2, x_arr)
    std = np.sqrt(raw_2 - raw_1 ** 2)

    # calculate values of lognormal distrib
    y_lognorm = lognormal(x_arr, raw_1, std)

    # calculate error
    rms_err = rms_error(y_lognorm, y)
    max_err = max_error(y_lognorm, y)
    chi_err = chi_error(y_lognorm, y)

    # generate samples
    samples = s.sampling.get_samples(100)
    sample_args = [ sam[:, np.newaxis] for sam in samples]
    q_arr = s.q(x_arr[None, :], *sample_args)

    #===========================================================================
    # Print
    #===========================================================================

    print 'check unity\t', np.trapz(y, x_arr)
    print 'mean\t\t', raw_1
    print 'std\t\t', std
    print 'rms error\t', rms_err
    print 'max error\t', max_err
    print 'chi error\t', chi_err

    #===========================================================================
    # Plot
    #===========================================================================
    # plot compounded distribution
    p.plot(x_arr, y, 'b-')
    # plot lognormal distribution, method of moments
    p.plot(x_arr, y_lognorm, color = 'red', linewidth = 2)
    # plot samples
    p.plot(x_arr, q_arr.T, color = 'gray')

    p.show()





if __name__ == '__main__':
    run()


