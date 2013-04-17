from numpy import pi, linspace, cos, arange, array, sin
import matplotlib.pyplot as plt

def F_(ii, p, al, fs, phi, t):
    f = 0
    for idx, i in enumerate(ii):
        f += al[idx] * sin(2. * pi * i * fs * t + phi[idx])
    return p * (f + 1)

def F(ii, p, al, fm, t):
    f = 0
    for idx, i in enumerate(ii):
        f += al[idx] * sin(2. * pi * i * fm * t)
    return p * (f + 1)


i = [1, 2, 3]
P = 750.
alpha = [1.6, .7, .2]
fm = 3.1
# Phi1 = [0, pi / 2., pi / 2., pi / 2.]
# Phi2 = [pi / 2., pi / 2., pi / 2., pi / 2.]
# Phi3 = [0, 0, 0, 0]
Tm = 1. / fm

t = arange(0., 140.02, 0.01)

y = F(i, P, alpha, fm, t)
# y[y < 0] = 0
mask = t % Tm
y[mask > mask.max() / 2.] = 0


plt.figure(0)
plt.plot(t, y)
plt.xlim(0, 1.2)


outfile = open("force1.mac", "w")
for i in range(1, len(t)):
    outfile.write("*SET, FORCE_VER(%i,%i),%f\n" % (i, 0, t[i - 1]))
    outfile.write("*SET, FORCE_VER(%i,%i),%f\n" % (i, 1, y[i - 1]))


outfile.close()

plt.show()


