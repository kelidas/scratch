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

from spirrid import make_ogrid
import numpy as np

evar_names = ['a', 'b', 'c']
evar_lst = [np.arange(1, 5, 1), np.arange(5, 10, 1), np.arange(10, 15, 1)]

e_ogrid = make_ogrid(evar_lst)

def f(a, b, c,):
    return a * b * c


def mu_q(*e):
    eargs = dict(zip(evar_names, e))
    res = f(**eargs)
    return res

otypes = [ float for i in range(len(evar_lst))]
mu_q_vec = np.vectorize(mu_q, otypes=[float])

print mu_q_vec(*e_ogrid)




