from numpy import pi, linspace, cos, sin, sum
import matplotlib.pyplot as plt

#def Fm( p, alpha, ii ):
#    f = 0
#    for idx, i in enumerate( ii ):
#        f += alpha[idx]
#    return p * ( f + 1 )

def F( ii, p, alpha, fmi, fs, phi, t ):
    Tp = 1. / fs
    C1 = 1. / fmi - 1
    if max ( ii ) == 3:
        C2 = p * ( 1 - alpha[1] )
    elif max ( ii ) == 4:
        C2 = p * ( 1 - alpha[1] + alpha[3] )

    Fm = p * ( sum( alpha ) + 1 )

    if ( t >= 0 and t < 0.04 * Tp ):
        return ( fmi * Fm - p ) / 0.04 / Tp * t + p
    elif ( t >= 0.04 * Tp and t < 0.06 * Tp ):
        return fmi * Fm * ( C1 * ( t - 0.04 * Tp ) / 0.02 / Tp + 1 )
    elif ( t >= 0.06 * Tp and t < 0.15 * Tp ):
        return Fm
    elif ( t >= 0.15 * Tp and t < 0.9 * Tp ):
        f = 0.
        for idx, i in enumerate( ii ):
            f += alpha[idx] * sin( 2. * pi * i * fs * ( t + 0.1 * Tp ) + phi[idx] )
        return p * ( f + 1 )
    elif ( t >= 0.9 * Tp and t < Tp ):
        return 10 * ( p - C2 ) * ( t / Tp - 1 ) + p
    else:
        tt = t - divmod( t, Tp )[0] * Tp
        return F( ii, p, alpha, fmi, fs, phi, tt )

i = [1., 2., 3., 4.]
P = 700.
alpha = [0.5, .2, .1, .05]
fmi = 1.12

fs = 2#1.79
Phi1 = [0., pi / 2., pi / 2., pi / 2.]
Phi2 = [0., pi / 2., pi, pi / 2.]
Phi3 = [0., 3. * pi / 2., pi , pi / 2.]

t = linspace( 0., 2., 1000 )
y = []
for val in t:
    y.append( F( i, P, alpha, fmi, fs, Phi3, val ) )

plt.figure( 0 )
plt.plot( t, y, "rx-" )
plt.ylim( 0, max( y ) * 1.1 )

#plt.figure(1)
#plt.plot( t, F(i, P, alpha, fs, Phi3, t ) )


plt.show()
