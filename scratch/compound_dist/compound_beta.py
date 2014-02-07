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
from compound_lab import rms_error, max_error, lognormal_pdf, chi_error, \
                    ks_error, lognormal_cdf, beta_par


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

def run(mu, cov, plot=True):

    # discretize the control variable (x-axis)
    x_arr = np.linspace(0, 10.0, 1000)[1:]

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q=BasicPDF(),
                e_arr=x_arr,
                n_int=100,
                tvars=dict(mu=mu,
                             cov=cov
                             ),
                sampling_type='TGrid',
                codegen_type='numpy',
                )
    # s.codegen.cached_dG = False
    # s.codegen.compiled_eps_loop = False

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
    ks_err = ks_error(lognorm_cdf, cpd_cdf)

    # generate samples
    samples = s.sampling.get_samples(20)
    sample_args = [ sam[:, np.newaxis] for sam in samples]
    q_arr = s.q(x_arr[None, :], *sample_args)

    emp_data = np.loadtxt('data_emp.txt', delimiter='\t')

    #===========================================================================
    # Print
    #===========================================================================

    print 'check unity\t', np.trapz(cpd_pdf, x_arr)
    print 'mean\t\t', raw_1
    print 'std\t\t', std
    print 'rms error\t', rms_err
    print 'max error\t', max_err
    print 'chi error\t', chi_err
    print 'ks error\t', ks_err

    #===========================================================================
    # Plot
    #===========================================================================
    if plot:
        p.figure()
        p.title(mu.type)
        # plot samples
        # p.plot(x_arr, q_arr.T, color = 'gray')
        for s in q_arr:
            p.plot(x_arr, s, color='gray', linewidth=mu.pdf((s * x_arr).sum() / 100.) * 5)
        # plot compounded distribution
        p.plot(x_arr, cpd_pdf, 'b-', label='cpd')
        # plot lognormal distribution, method of moments
        p.plot(x_arr, lognorm_pdf, color='red', linewidth=2, label='lognorm')
        p.plot(x_arr, lognormal_pdf(x_arr, np.mean(emp_data[:, 0]), np.std(emp_data[:, 0])), color='cyan', linewidth=2, label='lognorm_data')
        p.plot(x_arr, mu.pdf(x_arr), color='green', label='mu_dist')
        p.legend()

        p.figure()
        p.title(mu.type)
        p.plot(emp_data[:, 0], emp_data[:, 1], 'k-', linewidth=3, label='emp')
        p.plot(x_arr, cpd_cdf, 'b-', label='cpd')
        # plot lognormal CDF, method of moments
        p.plot(x_arr, lognorm_cdf, color='red', linewidth=2, label='lognorm')
        p.plot(x_arr, lognormal_cdf(x_arr, np.mean(emp_data[:, 0]), np.std(emp_data[:, 0])), color='cyan', linewidth=2, label='lognorm_data')
        p.legend()

        p.figure()
        p.title(mu.type)
        p.loglog(emp_data[:, 0], emp_data[:, 1], 'k-', linewidth=3, label='emp')
        p.loglog(x_arr, cpd_cdf, 'b-', label='cpd')
        p.loglog(x_arr, lognorm_cdf, color='red', linewidth=2, label='lognorm')
        p.loglog(x_arr, lognormal_cdf(x_arr, np.mean(emp_data[:, 0]), np.std(emp_data[:, 0])), color='cyan', linewidth=2, label='lognorm_data')
        p.legend()

    # p.show()
    return rms_err




if __name__ == '__main__':
    from pdistrib import beta_distr
    import os
    FILE_DIR = os.path.dirname(beta_distr.__file__)


    m_mu, std_mu = 3.2126, 0.655  # var = 0.429025
    alp, bet, a, b = beta_par(m_mu, std_mu, 0, 1e10)
    np.savetxt(os.path.join(FILE_DIR, 'distr_par.txt'), [[alp, bet]], delimiter=',')
    m_cov, std_cov = 0.17, .07  # 0.067
    print alp, bet

    cov = .17  # RV('norm', m_cov, std_cov)#RV('uniform', 0.049276, 0.29072) # 0.17

    run_args = dict(
                    beta=dict(mu=RV('beta_distr', loc=a, scale=(b - a)), cov=cov),
                    )

    run(**run_args['beta'])
#    from scipy.optimize import fsolve, brute, anneal
#
#    def residuum(b):
#        b = float(b)
#        alp, bet, a, b = beta_par(m_mu, std_mu, 0, b)
#        beta = dict(mu = RV('beta', shape = [alp, bet], loc = a, scale = (b - a)), cov = cov)
#        return run(plot = False, **beta)

    # f_vec = np.vectorize(residuum)
    # res = f_vec(np.linspace(3.4, 100, 1000))
    # print res
    # print np.min(res)
    # print np.argmin(res)

    # print fsolve(residuum, 20)
    # print brute(residuum, ((3.4, 20)))
    # print anneal(residuum, 10)

    p.show()
