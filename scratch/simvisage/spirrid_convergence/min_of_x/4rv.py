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

from etsproxy.traits.api import implements, Str
from scipy.special import erf
from spirrid import SPIRRID, Heaviside, RV, RF, IRF
from spirrid.extras import SPIRRIDLAB
import math
import numpy as np

#===========================================================================
# Response function
#===========================================================================
class fiber_tt_2p(RF):
    ur'''
   
    '''
    implements(IRF)

    title = Str('minimum of 4RVs')

    def __call__(self, e, x1, x2, x3, x4):
        return np.minimum(np.minimum(np.minimum(x1, x2), x3), x4)

    cython_code = '''
            q = np.minimum(np.minimum(np.minimum(x1, x2), x3), x4)
            '''

    weave_code = '''
            q = fmin(fmin(fmin(x1,x2),x3),x4);
            '''

def create_demo_object(fig_output_dir='fig'):

    # discretize the control variable (x-axis)
    e_arr = np.array([1.0])#np.linspace(0, 2.0, 80)

    # n_int range for sampling efficiency test
    powers = np.linspace(1, math.log(30, 10), 500)
    n_int_range = np.array(np.power(10, powers), dtype=int)

    #===========================================================================
    # Randomization
    #===========================================================================
    s = SPIRRID(q=fiber_tt_2p(),
                e_arr=e_arr,
                n_int=30,
                tvars=dict(x1=RV('weibull_min', 0, 1, 12),
                           x2=RV('weibull_min', 0, 1, 12),
                           x3=RV('weibull_min', 0, 1, 12),
                           x4=RV('weibull_min', 0, 1, 12),
                             ),
                #codegen_type='weave',
                sampling_type='TGrid'
                )
    from decimal import Decimal
    print Decimal(s.mu_q_arr[0])

    #===========================================================================
    # Exact solution
    #===========================================================================
    def mu_q_ex():
        from scipy.special import gamma
        n = 4
        return np.array([1. / (n * 12) * n ** (11. / 12.) * np.pi / (gamma(11. / 12.) * np.sin(np.pi / 12.))])

    print Decimal((s.mu_q_arr - mu_q_ex())[0])


    #===========================================================================
    # Lab
    #===========================================================================
    slab = SPIRRIDLAB(s=s, save_output=False, show_output=True,
                      dpi=300,
                      fig_output_dir=fig_output_dir,
                      plot_mode='subplots',
                      exact_arr=mu_q_ex(),
                      n_int_range=n_int_range,
                      extra_compiler_args=True,
                      le_sampling_lst=['LHS', 'PGrid'],
                      le_n_int_lst=[25, 30])

    return slab

if __name__ == '__main__':

    slab = create_demo_object()

    slab.configure_traits()
