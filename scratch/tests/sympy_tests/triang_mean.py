'''
Created on Feb 23, 2011

@author: kelidas
'''


from sympy import Symbol, cos, integrate, pprint, simplify, together, N
from sympy.abc import a, b, c, x


f1 = 2 * ( x - a ) / ( ( b - a ) * ( c - a ) )
f2 = 2 * ( b - x ) / ( ( b - a ) * ( b - c ) )

#pprint ( simplify( integrate( f1 * x, ( x, a, c ) ) + integrate( f2 * x, ( x, c, b ) ) ) )


f1 = 1 / ( b - a )

#pprint ( simplify( integrate( f1 * x, ( x, a, b ) ) ) )

pprint( simplify( ( a ** 3 - 3 * a * c ** 2 + 2 * c ** 3 ) / ( 3 * ( b - a ) * ( c - a ) )
                  + ( b ** 3 - 3 * b * c ** 2 + 2 * c ** 3 ) / ( 3 * ( b - a ) * ( b - c ) ) ) )
#pprint( simplify( ( a ** 3 - 3 * a * c ** 2 + 2 * c ** 3 ) / ( c - a ) ) )


from sympy import Integral, preview
preview( f1 )
#preview( simplify( ( a ** 3 - 3 * a * c ** 2 + 2 * c ** 3 ) / ( 3 * ( b - a ) * ( c - a ) )
#                  + ( b ** 3 - 3 * b * c ** 2 + 2 * c ** 3 ) / ( 3 * ( b - a ) * ( b - c ) ) ) )

x1 = Symbol( 'x1' )
x2 = Symbol( 'x2' )
x3 = Symbol( 'x3' )
x4 = Symbol( 'x4' )
x5 = Symbol( 'x5' )
f3 = ( x1 * x2 * x3 * x4 * x5 ) / ( ( x1 * x2 * x3 * x4 + x2 * x3 * x4 * x5 + x3 * x4 * x5 * x1 + x4 * x5 * x1 * x2 + x5 * x1 * x2 * x3 ) )

f = x1 * x2 / ( x1 + x2 )
pprint( f )
res = integrate( integrate( f, ( x1, 2, 5 ) ), ( x2, 2, 5 ) )
print N( res )

#pprint( f3 )
#vys = integrate( integrate( integrate( integrate( integrate( f3 / ( 34.642 * 5 ), ( x1, 32.679, 67.321 ) ), ( x2, 32.679, 67.321 ) ), ( x3, 32.679, 67.321 ) ), ( x4, 32.679, 67.321 ) ), ( x5, 32.679, 67.321 ) )
#print vys


