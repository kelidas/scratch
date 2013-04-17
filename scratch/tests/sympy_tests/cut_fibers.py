'''
Created on 24.3.2011

@author: Kelidas
'''


from sympy import sin, Symbol, cos, pprint, integrate, Rational, N, evalf
from sympy.mpmath import pi
ell = Symbol( 'ell' )
phi = Symbol( 'phi' )
L = Symbol( 'L' )
x = Symbol( 'x' )
le = Symbol( 'le' )

ff = sin( phi ) / L * ( Rational( 1, 2 ) * ell - x / cos( phi ) )

pprint( ff )

res = 2 * integrate( integrate( ff, ( x, 0, Rational( 1, 2 ) * ell * cos( phi ) ) ), ( phi, 0, Rational( 1, 2 ) * pi ) )
print res
print N( res )


from sympy import solve
from sympy.functions.special.delta_functions import Heaviside
fle = ( Rational( 1, 2 ) * ell - abs( x ) / cos( phi ) ) * Heaviside( Rational( 1, 2 ) * ell * cos( phi ) )

res3 = solve( fle - le, x )
pprint ( res3 )




