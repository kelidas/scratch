from sympy import Symbol, exp, Rational, integrate, simplify, pprint
import sympy.mpmath as mp

x = Symbol('x')
shape = Symbol('shape')
scale = Symbol('scale')
loc = Symbol('loc')

weib_cdf = Rational(1.0) - exp(-(x ** shape * scale ** (-shape)))

weib_cdf_refl = exp(x ** shape * scale ** (-shape))

w = integrate(weib_cdf_refl, x)

print(simplify(w))

pprint(simplify(exp(-exp(w))))

