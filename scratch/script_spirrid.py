#-------------------------------------------------------------------------------
#
# Copyright (c) 2012
# IMB, RWTH Aachen University,
# ISM, Brno University of Technology
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in the Spirrid top directory "licence.txt" and may be
# redistributed only under the conditions described in the aforementioned
# license.
#
# Thanks for using Simvisage open source!
#
#-------------------------------------------------------------------------------

from etsproxy.traits.api import HasTraits

from scipy.stats.distributions import norm
import numpy as np
import pylab as p # import matplotlib with matlab interface
import platform
import time

if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock

import os
os.environ['OPT'] = '-DNDEBUG -g -fwrapv -O3'

def main():
    n_rv = 2
    # set the mean and standard deviation of the two random variables
    m_la, std_la = 0.0, 1.0
    m_xi, std_xi = 0.0, 1.0

    # construct objects representing normal distribution
    pdistrib_la = norm(loc=m_la, scale=std_la)
    pdistrib_xi = norm(loc=m_xi, scale=std_xi)

    # for the evaluation of the probability density functions
    g_la = pdistrib_la.pdf
    g_xi = pdistrib_xi.pdf

    n_int = 2000 # number of discretization points

    th_min = pdistrib_la.ppf(1e-16)
    th_max = pdistrib_la.ppf(1 - 1e-16)
    # discretize the range (-1,1) symmetrically with n_int points
    #theta_arr = np.linspace(-(1.0 - 1.0 / n_int), 1.0 - 1.0 / n_int , n_int)
    d_la = (th_max - th_min) / n_int
    d_xi = (th_max - th_min) / n_int
    theta_arr = np.linspace(th_min + d_la * 0.5, th_max - d_la * 0.5 , n_int)

    # cover the random variable symmetrically around the mean 
    #theta_la = m_la + 50 * std_la * theta_arr
    #theta_xi = m_xi + 50 * std_xi * theta_arr
    theta_la = theta_arr
    theta_xi = theta_arr
    print theta_la, theta_xi

    # get the size of the integration cell
    #d_la = (100 * std_la) / n_int
    #d_xi = (100 * std_xi) / n_int

    print d_la, d_xi

    def Heaviside(x):
        ''' Heaviside function '''
        return x >= 0

    def q(eps, la, xi):
        '''  '''
        return np.exp(-la * la) + np.exp(-xi * xi)

    # prepare the sequence of the control strains in a numpy array
    eps_arr = np.array([1.0])#np.linspace(0, 1.2, 100)

    # define an array of the same size as e_arr
    mu_q_arr = np.zeros_like(eps_arr)

    def mu_q_loops(eps):
        # define an array of the same size as eps_arr initialized with zeros
        mu_q_arr = np.zeros_like(eps_arr)
        # loop over the control variable (strain)
        for i, eps in enumerate(eps_arr):
            mu_q = 0.0
            # loops over the arrays of lambda and xi values
            for la in theta_la:
                for xi in theta_xi:
                    dG = (g_la(la - d_la / 2.) + g_la(la + d_la / 2.)) / 2. *\
                     (g_xi(xi - d_xi / 2.) + g_xi(xi + d_xi / 2.)) / 2. * d_la * d_xi#g_la(la) * g_xi(xi) * d_la * d_xi
                    mu_q += q(eps, la, xi) * dG
            mu_q_arr[ i ] = mu_q


    start_time = sysclock()
    #mu_q_arr = mu_q_loops(eps_arr)
    print 'loop-based: elapsed time', sysclock() - start_time
    #print 'precision', mu_q_arr - np.array([np.sqrt(3)/3.*2.])

    dG_la = g_la(theta_la) * d_la
    dG_xi = g_xi(theta_xi) * d_xi
    dG_grid = dG_la[:, np.newaxis] * dG_xi[np.newaxis, :]

    def mu_q(eps):
        ''' Summation / integration  over the random domain '''
        q_grid = q(eps, theta_la[:, np.newaxis], theta_xi[np.newaxis, :])
        # element by element product of two (n,n) arrays
        q_dG_grid = q_grid * dG_grid
        return np.sum(q_dG_grid)

    mu_q_vct = np.vectorize(mu_q)
    start_time = sysclock()
    mu_q_arr = mu_q_vct(eps_arr)
    print 'Regular grid of random variables: elapsed time', sysclock() - start_time
    print 'precision', mu_q_arr - np.array([np.sqrt(3) / 3.*2.])

    code = '''
    double eps = e;
    double mu_q=0;
    double q=0;
    #line 100
    for( int i_la = 0; i_la < n_la; i_la++){
        double la = la_flat( i_la );
        for( int i_xi = 0; i_xi < n_xi; i_xi++){
            double xi = xi_flat( i_xi );
        double dG = dG_grid(i_la,i_xi);
                {
                                  q = exp(-la*la) + exp(-xi*xi);
                            }
                
                        mu_q +=  q * dG;
    };
    };
    return_val = mu_q;        /*I would like to fill in changed locals and globals here...*/      
    '''
    from scipy import weave
    mu_q_arr = np.zeros_like(eps_arr)

    arg_names = ['e', 'n_la', 'n_xi', 'xi_flat', 'la_flat', 'dG_grid']
    local_dict = {'e':1.0,
                 'n_la':n_int,
                 'n_xi':n_int,
                 'xi_flat':theta_xi,
                 'la_flat':theta_la,
                 'dG_grid':dG_grid}

    for i_eps, eps in enumerate(eps_arr):
        mu_q_arr[i_eps] = weave.inline(code, arg_names, local_dict,
                                 type_converters=weave.converters.blitz)

    print 'precision', mu_q_arr - np.array([np.sqrt(3) / 3.0 * 2.])












    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='blue', label='Tgrid')
    p.subplot(122)
    expander = np.ones((n_int, n_int), dtype=int)
    p.plot((theta_la[np.newaxis, :] * expander).flatten(),
            (theta_xi[:, np.newaxis] * expander).flatten(),
            'b.', label='Tgrid')


    def get_mu_q(q, dG, *theta):
        ''' Return a method integrating the function q
        with variables *theta associated with probabilities dG
        '''
        def mu_q(eps):
            '''Template for the evaluation of the mean response.
            '''
            Q_dG = q(eps, *theta)
            Q_dG *= dG # in-place multiplication
            return np.sum(Q_dG)
        return np.vectorize(mu_q)

    # get the total number of integration points (n_int equal for both variables)
    n_sim = n_int ** n_rv

    #===========================================================================
    # Grid of constant probabilities
    #===========================================================================
    # generate the equidistant array of sampling probabilities
    pi_arr = np.linspace(0.5 / n_int, 1. - 0.5 / n_int, n_int)
    # use ppf (percent point function) returning inverse probabilities
    theta_la = pdistrib_la.ppf(pi_arr)
    theta_xi = pdistrib_xi.ppf(pi_arr)
    # instantiate the above template with the randomization
    mu_q = get_mu_q(q, 1.0 / n_sim, theta_la[:, np.newaxis], theta_xi[np.newaxis, :])
    start_time = sysclock()
    # estimate mean response
    mu_q_arr = mu_q(eps_arr)
    print 'Grid of constant probabilities: elapsed time', sysclock() - start_time
    print 'precision', mu_q_arr - np.array([np.sqrt(3) / 3.*2.])

    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='cyan', label='Pgrid')
    p.subplot(122)
    p.plot((theta_la[np.newaxis, :] * expander).flatten(),
            (theta_xi[:, np.newaxis] * expander).flatten(),
            'co', label='Pgrid')


    #===========================================================================
    # Monte-Carlo implementation
    #===========================================================================
    # generate n_sim random realizations
    theta_la_rvs = pdistrib_la.rvs(n_sim)
    theta_xi_rvs = pdistrib_xi.rvs(n_sim)
    # instantiate the integration template with the randomization
    mu_q_e_rvs = get_mu_q(q, 1.0 / n_sim, theta_la_rvs, theta_xi_rvs)
    start_time = sysclock()
    # estimate mean response
    mu_q_arr = mu_q_e_rvs(eps_arr)
    print 'Monte-Carlo: elapsed time', sysclock() - start_time
    print 'precision', mu_q_arr - np.array([np.sqrt(3) / 3.*2.])

    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='red', label='Monte-Carlo')
    p.subplot(122)
    p.plot(theta_la_rvs, theta_xi_rvs, 'rD', label='Monte-Carlo')


    #===========================================================================
    # LHS 
    #===========================================================================
    # generate n_sim values of random nature (n_sim as above)
    pi_arr = np.linspace(0.5 / n_sim, 1. - 0.5 / n_sim, n_sim)
    # use ppf (percent point function) returning inverse probabilities
    theta_la_ppf = pdistrib_la.ppf(pi_arr)
    theta_xi_ppf = pdistrib_xi.ppf(pi_arr)
    # make random permutations of both arrays
    theta_la = theta_la_ppf # np.random.permutation(theta_la_ppf)
    theta_xi = np.random.permutation(theta_xi_ppf)
    # instantiate the above template with the randomization
    mu_q = get_mu_q(q, 1.0 / n_sim, theta_la, theta_xi)
    start_time = sysclock()
    # estimate mean response
    mu_q_arr = mu_q(eps_arr)
    print 'LHS: elapsed time', sysclock() - start_time
    print 'precision', mu_q_arr - np.array([np.sqrt(3) / 3.*2.])

    code = '''
    double eps = e;
    double mu_q=0;
    double q=0;
    #line 100
    for( int i_la = 0; i_la < n_la; i_la++){
        double la = la_flat( i_la );
        for( int i_xi = 0; i_xi < n_xi; i_xi++){
            double xi = xi_flat( i_xi );
        //double dG = dG_grid(i_la,i_xi);
                {
                                  q = exp(-la*la) + exp(-xi*xi);
                            }
                
                        mu_q +=  q * 1.0/(n_la* n_xi);
    };
    };
    return_val = mu_q;    
    '''
    mu_q_arr = np.zeros_like(eps_arr)

    arg_names = ['e', 'n_la', 'n_xi', 'xi_flat', 'la_flat']
    local_dict = {'e':1.0,
                 'n_la':n_int ** 2,
                 'n_xi':n_int ** 2,
                 'xi_flat':theta_xi,
                 'la_flat':theta_la}


    for i_eps, eps in enumerate(eps_arr):
        mu_q_arr[i_eps] = weave.inline(code, arg_names, local_dict,
                                 type_converters=weave.converters.blitz)

    print 'precision', mu_q_arr - np.array([np.sqrt(3) / 3.0 * 2.])


    exit()








    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='green', label='LHS')
    p.subplot(122)
    p.plot(theta_la, theta_xi, 'go', label='LHS')

    p.subplot(121)
    p.legend()
    p.xlabel('$\\varepsilon$', fontsize=24)
    p.ylabel('$q$', fontsize=24)


    ############################## Discretization grids ########################
    p.subplot(122)
    p.ylabel('$\\theta_{\\xi}$', fontsize=24)
    p.ylim(0.5, 1.5)
    p.xlim(5, 15)
    p.xlabel('$\\theta_{\lambda}$', fontsize=24)
    p.legend()

    p.show()

if __name__ == '__main__':
    main()
