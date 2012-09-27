import numpy as np
cimport numpy as np
ctypedef np.double_t DTYPE_t
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def mu_q(np.ndarray[DTYPE_t, ndim=1] e_arr,np.ndarray[DTYPE_t, ndim=1] la_flat,np.ndarray[DTYPE_t, ndim=1] xi_flat):
    cdef double mu_q
    cdef double la, xi, eps, dG, q
    cdef int i_la, i_xi
    cdef np.ndarray mu_q_arr = np.zeros_like( e_arr )
    for i_eps from 0 <= i_eps < 80:
        eps = e_arr[i_eps]
        mu_q = 0
        dG = 0.000100000000000000004792173602385929598312941379845142364501953125
        for i from 0 <= i < 10000:
            la = la_flat[i]
            xi = xi_flat[i]
            
            # Computation of the q( ... ) function
            if eps < 0 or eps > xi:
                q = 0.0
            else:
                q = la * eps
            
            mu_q += q * dG

        mu_q_arr[i_eps] = mu_q
    return mu_q_arr

