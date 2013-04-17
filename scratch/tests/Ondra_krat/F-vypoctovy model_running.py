# -*- coding: cp1250 -*-
from numpy import pi, linspace, cos, sin, sum, arange
import matplotlib.pyplot as plt

# def Fm( p, alpha, ii ):
#    f = 0
#    for idx, i in enumerate( ii ):
#        f += alpha[idx]
#    return p * ( f + 1 )


#   MŮJ NEFUNKČNÍ NÁSTŘEL

def F(ii, p, al, fs, phi, t):
    f = 0
    for idx, i in enumerate(ii):
        f += al[idx] * cos(2. * pi * i * fs * t + phi[idx])
        if (f < 0):
            f += 0
    return p * (f + 1)






i = [1., 2., 3., 4.]
P = 700.
alpha = [1.7, .7, .2, .05]
fmi = 1.12

fs = 2.3
Phi1 = [0., pi / 2., pi / 2., pi / 2.]
Phi2 = [0., pi / 2., pi, pi / 2.]
Phi3 = [0., -pi / 2., -pi, -3. * pi / 2.]

t = arange(0., 350.02, 0.01)
y = []
for val in t:
    y.append(F(i, P, alpha, fs, Phi2, val))

plt.figure(0)
plt.plot(t, y,)
plt.ylim(0, max(y) * 1.1)
plt.xlim(0, 2)
# plt.figure(1)
# plt.plot( t, F(i, P, alpha, fs, Phi3, t ) )

outfile = open("force2.mac", "w")
for i in range(1, len(t)):
    outfile.write("*SET, FORCE_VER(%i,%i),%f\n" % (i, 0, t[i - 1]))
    outfile.write("*SET, FORCE_VER(%i,%i),%f\n" % (i, 1, y[i - 1]))

outfile.close()


plt.show()
