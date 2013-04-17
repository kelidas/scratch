

import numpy as np
from numpy import piecewise, linspace, sqrt
import matplotlib.pyplot as plt

# design ground acceleration on type A ground
agr = 0.05
gamma_1 = 1.2 # vyznamnost stavby
g = 9.81
ag = agr * g * gamma_1
# dynamic amplification factor (typical value 2.5)
beta0 = 2.5

dzeta = 5  # zakladni hodnota tlumeni 5%
# damping correction factor
eta = sqrt(10. / (5. + dzeta))
if eta >= 0.55:
    print 'eta =', eta
else:
    print 'eta is smaller then 0.55'

# lower limit of the period of the constant acceleration branch
Tb = 0.05 #0.15
# upper limit of the period of the constant acceleration branch
Tc = 0.25 #.5
# the value defining the beginning of the constant displacement response range of the spectrum
Td = 1.2 #2.
# soil factor
S = 1.35 #1#.75

# elastic response spectrum functions
def Sea(t):
    return ag * S * (1.0 + t / Tb * (beta0 * eta - 1.0))

def Seb(t):
    return ag * S * beta0 * eta

def Sec(t):
    return ag * S * beta0 * eta * Tc / t

def Sed(t):
    return ag * S * beta0 * eta * Tc * Td / t ** 2


t = linspace(0.02, 4, 1000)
y = piecewise(t, [(0 <= t) * (t <= Tb),
                   (Tb < t) * (t <= Tc),
                   (Tc < t) * (t <= Td),
                   (Td < t) * (t <= 4)],
                [lambda t: Sea(t),
                 lambda t: Seb(t),
                 lambda t: Sec(t),
                 lambda t: Sed(t)])

data = np.loadtxt('hradil_spectrum.txt')

plt.subplot(121)
plt.plot(t, y) # y / ag
plt.plot(data[:, 0], data[:, 1], 'r-', label='hradil')
plt.subplot(122)
plt.plot(1. / t, y) # y / ag

plt.show()







