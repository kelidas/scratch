

import numpy as np
from scipy.stats import beta
import pylab as p

def beta_par(mu, sig, a, b):
    s = (mu - a) / (b - a)
    e = (b - a) / sig
    q = s * s * e * e
    alpha = q * (1 - s) - s
    beta_ = q * (s - 2) + s * (1 + e * e) - 1
    return alpha, beta_, a, b

beta_par_vec = np.vectorize(beta_par)

mu = 3.2126
sig = 0.655
a = 0.0
b = np.linspace(3.4, 100, 1000)

#rv = beta(
par = np.array(beta_par_vec( mu,sig,a,b))

x = np.linspace(0,10,1000)

for i in par.T:
    rv = beta(i[0], i[1], loc= i[2], scale=(i[3]-i[2]))
    p.plot(x, rv.pdf(x))

p.figure()
b = np.linspace(100, 1e10, 1000)
par = np.array(beta_par_vec( mu,sig,a,b))
for i in par.T:
    rv = beta(i[0], i[1], loc= i[2], scale=(i[3]-i[2]))
    p.plot(x, rv.pdf(x))

p.show()
