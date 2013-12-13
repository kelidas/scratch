# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# from IPython.display import display, HTML
import os
import numpy as np
import mpmath as mp
import matplotlib.pyplot as plt
import sympy as sp
# sp.init_session()
# x, y, z, t = sp.symbols('x y z t')
# k, m, n = sp.symbols('k m n', integer=True)
# f, g, h = sp.symbols('f g h', cls=sp.Function)
# sp.init_printing(use_latex=True)
plt.rc('savefig', dpi=200)
plt.rc('savefig', format='png')
mp.mp.dps = 1000
MPF_ONE = mp.mpf('1')
# %load_ext sympy.interactive.ipythonprinting

# <markdowncell>

# Names of variables
# ------------------
# * $s, m, l =$ scale, shape and location of Weibull distribution of filament
# * $s_f, m_f, l_f =$ scale, shape and location of Weibull distribution of fit of differentiated Weibull plot Gn

# <codecell>

x, y, z, s, m, l, n, t = sp.symbols('x y z s m l n t')
s_f = sp.Symbol('s_f')
m_f = sp.Symbol('m_f')
l_f = sp.Symbol('l_f')

# <markdowncell>

# Weibull distribution
# --------------------

# <codecell>

weib_cdf = 1 - sp.exp(-((x - l) / s) ** m)
# display(weib_cdf)

# <markdowncell>

# Weibull fit integration
# -----------------------
# * weib_ref = Weibull distribution reflected accross the axis $y$
# * derGn = denormalized weib_ref
# * WGn_l = integral of derGn
# * x = ln(x)

# <codecell>

weib_ref = 1 - sp.exp(-((-x - l_f) / s_f) ** m_f)
derGn = m * (n - 1) * weib_ref + m
WGn_l = sp.integrate(derGn.subs({m_f:1}), x)
# http://gamma.sympy.org/, http://integrals.wolfram.com/index.jsp?expr=%28m*n-m%29*%281+-+Exp[-%28%28-x-l%29%2Fy%29^z]%29%2Bm&random=false
WGn_shape = (m * (n * x * ((-((l_f + x) / s_f)) ** m_f) ** m_f ** (-1) * m_f + (-1 + n) * (l_f + x) * sp.uppergamma(m_f ** (-1), (-((l_f + x) / s_f)) ** m_f))) / (((-((l_f + x) / s_f)) ** m_f) ** m_f ** (-1) * m_f)
# display(sp.simplify(WGn_l))
# display(WGn_shape)  # sp.simplify(WGn_shape)

# <codecell>

# HTML('<iframe src=http://integrals.wolfram.com/index.jsp?expr=%28m*n-m%29*%281+-+Exp[-%28%28-x-l%29%2Fy%29^z]%29%2Bm&random=false width=900 height=400></iframe>')

# <markdowncell>

# Table of fitted parameters
# --------------------------

# <codecell>

# shape, scale, n_fil, l_fit, s_fit
table = np.array([[6.0, 1.0, 10.0, 0.37566873, 0.760418],
                  [6.0, 1.0, 20.0, 0.39934985, 0.8447352],
                  [6.0, 1.0, 100.0, 0.43953691, 0.94930124],
                  [10.0, 1.0, 10.0, 0.28490917, 0.77294302],
                  [10.0, 1.0, 20.0, 0.28722278, 0.85757224],
                  [10.0, 1.0, 100.0, 0.30900391, 0.95354311], ])
idx = 0

# <markdowncell>

# Database data
# -------------

# <codecell>

# rec_dir = r'/media/raid/rsync_backups/recursion_database/'
rec_dir = r'/media/data/Documents/postdoc/2013/rekurze/recursion_database/'
# rec_dir = r'E:\Documents\postdoc\2013\rekurze\recursion_database'
shape = table[idx, 0]
scale = table[idx, 1]
n_fil = table[idx, 2]
m_dir = 'm=%05.1f' % shape
n_dir = 'm=%05.1f_n=%04d' % (shape, n_fil)

# <codecell>

gn_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-gn_wp' + '.npy'))
norm_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-norm_wp' + '.npy'))
weibr_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-weibr_wp' + '.npy'))
weibl_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-weibl_wp' + '.npy'))
ln_x = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-ln_x' + '.npy'))
sn = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-sn' + '.npy')).tolist()

# <markdowncell>

# Plot
# ----

# <codecell>

from matplotlib.ticker import FuncFormatter
def form3(x, pos):
    mp.mp.dps = 1000
    return '%s' % mp.nstr((MPF_ONE - mp.exp(-mp.exp(x))), 6)
formatter = FuncFormatter(form3)

# <codecell>

l_fit = table[idx, 3]
s_fit = table[idx, 4]
sr = scale / n_fil ** (1.0 / shape)
wgn_l = np.array([WGn_l.subs({x:lx, n:n_fil, l_f:l_fit, s_f:s_fit, m:shape}) for lx in ln_x[ln_x <= -l_fit]])
c1 = -wgn_l[-1] + sp.log(-sp.log(1 - weib_cdf.subs({x:np.exp(-l_fit), l:0.0, s:sr, m:shape})))
print c1
axes = plt.figure().add_subplot(111)
axes.plot(ln_x, gn_wp, 'b-', label='Gn')
axes.plot(ln_x[ln_x <= -l_fit], wgn_l + float(c1), 'g-', label='Gn_fit')
axes.plot(ln_x, norm_wp, 'k--', label='Norm')
axes.plot(ln_x, weibr_wp, 'r--', label='Weibr')
axes.legend(loc='best')
axes.grid()
axes.yaxis.set_major_formatter(FuncFormatter(formatter))

# <markdowncell>

# Table of fitted parameters for 3par Weibull
# --------------------------

# <codecell>

# shape, scale, n_fil, l_fit, s_fit
# table = np.array([[6.0, 1.0, 10.0, 0.1442213, 1.04930995, 1.4773259],
#                   [6.0, 1.0, 20.0, 0.25432229, 1.03137655, 1.27682538],
#                   [6.0, 1.0, 100.0, 0.39886882, 1.00474437, 1.07867128],
#                   [10.0, 1.0, 10.0, 0.13591634, 0.96693703, 1.32024471],
#                   [10.0, 1.0, 20.0, 0.1943415 , 0.98158641, 1.18671307],
#                   [10.0, 1.0, 100.0, 0.28391416, 0.9875614 , 1.04881256], ])

table = np.loadtxt('txt_data/weib_diff_fit.txt', delimiter=';')
# <codecell>
shape = 50
n_fil = 100

m_dir = 'm=%05.1f' % shape
n_dir = 'm=%05.1f_n=%04d' % (shape, n_fil)

# <codecell>

gn_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-gn_wp' + '.npy'))
norm_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-norm_wp' + '.npy'))
weibr_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-weibr_wp' + '.npy'))
weibl_wp = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-weibl_wp' + '.npy'))
ln_x = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-ln_x' + '.npy'))
sn = np.load(os.path.join(rec_dir, m_dir, n_dir, n_dir + '-sn' + '.npy')).tolist()

mask = np.logical_and(table[:, 0] == shape, table[:, 1] == n_fil)
l_fit = table[:, 2][mask]
s_fit = table[:, 3][mask]
m_fit = table[:, 4][mask]
k = shape * n_fil
q = -shape * n_fil * mp.log(sn)
print sn, shape, scale, n_fil
c = sp.Symbol('c')
WGn_m_asym = WGn_shape + c - k * x - q
res = sp.limit(WGn_m_asym.subs({n:n_fil, l_f:l_fit, s_f:s_fit, m_f:m_fit, m:shape}), x, -sp.oo)
print res, sp.solve(res, c)

# print sp.limit(WGn_m_asym.subs({n:n_fil, l_f:l_fit, s_f:s_fit, m_f:m_fit, m:shape}) / x, x, -sp.oo)

# <codecell>

sr = scale / n_fil ** (1.0 / shape)
wgn_l = np.array([np.complex(WGn_shape.subs({x:lx, n:n_fil, l_f:l_fit, s_f:s_fit, m_f:m_fit, m:shape}).evalf() + q) for lx in ln_x])
# c1 = -wgn_l[-1] + sp.log(-sp.log(1-weib_cdf.subs({x:np.exp(-l_fit), l:0.0, s:sr, m:shape})))
# print c1
axes = plt.figure().add_subplot(111)
axes.plot(ln_x, gn_wp, 'b-', label='Gn')

axes.plot(ln_x, np.real(wgn_l), 'g-', label='Gn_fit')
# axes.plot(ln_x, norm_wp, 'k--', label='Norm')
# axes.plot(ln_x, weibr_wp, 'r--', label='Weibr')
axes.plot(ln_x, weibl_wp, 'r--', label='Weibl')
# axes.legend(loc='best')
axes.grid()
axes.yaxis.set_major_formatter(FuncFormatter(formatter))

plt.show()


