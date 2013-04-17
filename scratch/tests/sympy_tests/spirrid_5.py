'''
Created on Feb 23, 2011

@author: kelidas
'''


from sympy import Symbol, cos, integrate, pprint, simplify, together, \
                 N, exp, diff, preview, sqrt, oo, expand, Heaviside, evalf
from sympy.abc import E, A, x, e
from sympy.mpmath import pi
import numpy as np

lambd = Symbol( 'lambd' )
xi = Symbol( 'xi' )
th = Symbol( 'th' )


s = 0.2e-1
m = 10.0
lmx = 0.2
lmn = 0
Emx = 85e9
Emn = 70e9
tmx = 0.01
tmn = 0
Amx = 5.309e-10
Amn = 1.593e-10


F = 1 - exp( -( xi / s ) ** m )
f = diff( F, xi )

m_xi, std_xi = 0.019027, 0.0022891
f = 1. / ( std_xi * sqrt( 2. * pi ) ) * exp( -( xi - m_xi ) ** 2 / ( 2. * std_xi ** 2 ) )

#f = .1753101225e18 * exp( -3631.121554 * xi ) * exp( 95420.2331974697 * xi ** 2 )

print expand( f )
pprint( f )
#preview( f )
#print N( integrate( f, ( xi, -oo, oo ) ) )

eps_ = ( e - th * ( 1 + lambd ) ) / ( ( 1 + th ) * ( 1 + lambd ) )
q = E * A * eps_  # * Heaviside( xi - eps_ )

#preview( q )



res = integrate( 
                integrate( 
                          integrate( 
                                    integrate( 
                                              integrate( 1,
                                                         ( xi, eps_, .02 ) ) * E ,
                                              ( E, Emn, Emx ) ) * A,
                                    ( A, Amn, Amx ) ) * eps_,
                          ( th, tmn, tmx ) ),
                ( lambd, lmn, lmx ) ) #* 1. / ( ( lmx - lmn ) * ( Emx - Emn ) * ( Amx - Amn ) * ( tmx - tmn ) )

print  res






#mu_q_5 = ( integrate( 
#             integrate( 
#                 integrate( 
#                     integrate( 
#                         integrate( 
#                            q * f * 1. / ( ( lmx - lmn ) * ( Emx - Emn ) * ( Amx - Amn ) * ( tmx - tmn ) ),
#                        ( xi, eps_, oo ) ),
#                        ( th, tmn, tmx ) ),
#                        ( E, Emn, Emx ) ),
#                        ( A, Amn, Amx ) ),
#                        ( lambd, lmn, lmx ) ) )
#
#print mu_q_5

