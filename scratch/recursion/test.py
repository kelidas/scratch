
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
from database_prep import DATABASE_DIR

# dn_slope obtained by linear regression [30:] vs shape parameter
data = np.loadtxt(os.path.join('txt_data', 'shape-vs-dn_slope.txt'), skiprows=1)
m = data[:, 0]
s = data[:, 1]
slope, intercept, r_value, p_value, std_err = stats.linregress(m, s)
print slope, intercept
print r_value ** 2
plt.plot(m, s, 'bx-')
plt.plot(m, slope * m + intercept, 'r-')
plt.show()


d = os.path.join(DATABASE_DIR, 'm=6.0')
name = 'n=0010_m=6.0'

def fit_data_diff(part_name):
    from scipy.optimize import leastsq
    ln_x_diff = np.load(part_name + '-ln_x_diff.npy').astype(float)
    gn_diff = np.load(part_name + '-gn_diff.npy').astype(float)
    norm_diff = np.load(part_name + '-norm_diff.npy').astype(float)
    # FIT data
    def f_weib(a, b):
        z = (x / a) ** b
        ret = np.piecewise(z,
                [z < 0, z <= 10 ** (-12), z > 10 ** (-12)],
                 [lambda z: 0, lambda z: z - 0.5 * z * z + 1 / 6. * z ** 3 - 1 / 24. * z ** 4, lambda z: 1. - np.exp(-z) ])
        return ret[::-1]

    def f_gumb(a, b):
        return np.exp(-np.exp(-(-x - a) / b))

    def f_gev(a, b, c):
        return np.exp(-(1 + a * ((-x - b) / c)) ** (-1.0 / a))

    def residuals(p, y, x):
        err = y - f_gev(*p)
        return err

    p0 = [1., 1., 1.]
    mask = ln_x_diff < -.0
    x = ln_x_diff[mask]
    gn_diff = gn_diff[mask]
    plsq = leastsq(residuals, p0, args=(gn_diff, x))  # , ftol=1.49012e-12, xtol=1.49012e-12, maxfev=10000)
#    np.savetxt('x.txt', data.x)
#    np.savetxt('lnx.txt', data.x)
#    np.savetxt('wpcdfx.txt', data.wp_cdf_x)
    print 'plsq', plsq
    # np.save(data.inputfile[:-4] + '_plsq.npy', plsq[0])
    plt.figure(0)
    plt.plot(x, gn_diff, 'k-')
    plt.plot(ln_x_diff, norm_diff, 'g--', linewidth=.5)
    plt.plot(x, f_gev(*plsq[0]), 'r')

    plt.show()
fit_data_diff(os.path.join(d, name, name))


ln_x = np.load(os.path.join(d, name, name) + '-ln_x.npy')
wp_gn = np.load(os.path.join(d, name, name) + '-wp_gn.npy')
#np.savetxt('export.txt', [ln_x, wp_gn])
plt.plot(ln_x, wp_gn)
plt.show()
