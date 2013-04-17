from numpy import pi, linspace, cos, sin
import matplotlib.pyplot as plt

def F( p, al, fs, phi, t ):
    f = 0
    for i in [1, 2, 3, 4]:
        f += al[i - 1] * cos( 2. * pi * i * fs * t + phi[i - 1] )
    return p * ( f + 1 )


P = 700.
alpha = [0.5, .2, .1, .05]
fs = 1.79
Phi1 = [0, pi / 2., pi / 2., pi / 2.]
Phi2 = [0, pi / 2., pi, pi / 2.]

t = linspace( 0, 2., 1000 )


plt.plot( t, F( P, alpha, fs, Phi1, t ) )
plt.show()
