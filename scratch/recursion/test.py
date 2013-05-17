import numpy as np
import matplotlib.pyplot as plt


# dk_3 = np.load('dk_3.npy')
# dk_4 = np.load('dk_4.npy')
#
# # gn_3 = np.load('gn_3.npy')
# # gn_4 = np.load('gn_4.npy')
#
# # print dk_3, dk_4
#
# # print np.nansum(dk_4.astype(float), axis=1)
# x = np.array([ 47.074290 , 6861.935326, 30417603.583043])
#
# y = np.array([ 128., 4.72463547e+04, 3.04176046e+07])
#
# plt.plot(x, y)
# plt.show()




from sympy import Symbol, exp, Rational, integrate, simplify, pprint, solve, log, diff
import sympy.mpmath as mp

x = Symbol('x')
y = Symbol('y')
n = Symbol('n')
shape = Symbol('shape')
scale = Symbol('scale')
loc = Symbol('loc')
lgx = Symbol('lgx')

weib_cdf = Rational(1.0) - exp(-(x ** shape * scale ** (-shape)))

shape = 1
derGn = shape * (n - 1) * (1 - exp(-((-lgx - loc) / scale) ** shape)) + shape
WGn = simplify(integrate(derGn, lgx))
pprint(WGn)

shape = 1
derGn = shape * (n - 1) * (1 - exp(-((-log(x) - log(loc)) / scale) ** shape)) + shape
WGn = simplify(integrate(derGn, x))
pprint(WGn)

# print simplify(diff(log(-log(1 - weib_cdf)), x))

# print solve(weib_cdf - y, scale)
#
# weib_cdf = Rational(1.0) - exp(-((x) ** shape))
#
# print solve(weib_cdf - y, shape)
#
# weib_cdf_refl = exp(x ** shape * scale ** (-shape))
#
# w = integrate(weib_cdf_refl, x)
#
# print(simplify(w))
#
# pprint(simplify(exp(-exp(w))))

