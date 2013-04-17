from numpy import *
from matplotlib.ticker import FuncFormatter
import pylab as p

# I'm used to  the ln notation for the natural log
from numpy import log as ln

# Paramters
beta = 5.2
eta = 12

# Genrate 10 numbers following a Weibull distribution
x = eta * random.weibull(beta, size=10)
F = 1 - exp(-(x / eta) ** beta)

# Estimate Weibull parameters
lnX = ln(x)
lnF = ln(-ln(1 - F))
a, b = polyfit(lnF, lnX, 1)
beta0 = 1 / a
eta0 = exp(b)

# ideal line
F0 = array([1e-3, 1 - 1e-3])
x0 = eta0 * (-ln(1 - F0)) ** (1 / beta0)
lnF0 = ln(-ln(1 - F0))


# Weibull plot
p.figure()
ax = p.subplot(111)
p.semilogx(x, lnF, "bs")
p.plot(x0, lnF0, 'r-', label="beta= %5G\neta = %.5G" % (beta0, eta0))
p.grid()
p.xlabel('x')
p.ylabel('Cumulative Distribution Function')
p.legend(loc='lower right')

# ticks
def weibull_CDF(y, pos):
    return "%G %%" % (100 * (1 - exp(-exp(y))))

formatter = FuncFormatter(weibull_CDF)
ax.yaxis.set_major_formatter(formatter)

yt_F = array([ 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5,
           0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
yt_lnF = ln(-ln(1 - yt_F))
p.yticks(yt_lnF)

p.show()

from numpy import log2
import matplotlib.pyplot as plt

from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms

class CustomScale(mscale.ScaleBase):
    name = 'custom'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        self.thresh = None  #thresh

    def get_transform(self):
        return self.CustomTransform(self.thresh)

    def set_default_locators_and_formatters(self, axis):
        pass

    class CustomTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            return 10 ** (a / 10)

        def inverted(self):
            return CustomScale.InvertedCustomTransform(self.thresh)

    class InvertedCustomTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            return log2(a) * (10 / log2(10))

        def inverted(self):
            return CustomScale.CustomTransform(self.thresh)


mscale.register_scale(CustomScale)

xdata = [log2(x) * (10 / log2(10)) for x in range(1, 11)]
ydata = range(10)
plt.plot(xdata, ydata)

#plt.gca().set_xscale('custom')
plt.show()



import numpy as np
from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import Formatter, FixedLocator, FuncFormatter

class EscalaAcumuladaGumbel(mscale.ScaleBase):

    name = 'gumbel'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        thresh = kwargs.pop("thresh", 1.0)
        if thresh >= 1.1:
            raise ValueError("thresh must be less than 1.1")
        self.thresh = thresh

    def get_transform(self):
        return self.TransformacionAcumuladaGumbel(self.thresh)

    def set_default_locators_and_formatters(self, axis):
        class DegreeFormatter(Formatter):
            def __call__(self, x, pos=None):
                # \u0025 : simbolo %
                return "%d%%" % (x * 0.02)
        axis.set_major_locator(FixedLocator(np.arange(0.0, 1.0, 0.02)))
        axis.set_major_formatter(DegreeFormatter())
        axis.set_minor_formatter(DegreeFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(vmin, -self.thresh), min(vmax, self.thresh)

    class TransformacionAcumuladaGumbel(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            masked = ma.masked_where((a < -self.thresh) | (a > self.thresh), a)
            if masked.mask.any():
                return ma.exp(-np.exp(-a))
            else:
                return np.exp(-np.exp(-a))

        def inverted(self):
            return EscalaAcumuladaGumbel.TransformacionInversaAcumuladaGumbel(self.thresh)

    class TransformacionInversaAcumuladaGumbel(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            return -np.log(-np.log(a))

        def inverted(self):
            return EscalaAcumuladaGumbel.TransformacionAcumuladaGumbel(self.thresh)

mscale.register_scale(EscalaAcumuladaGumbel)

class GumbelScale(mscale.ScaleBase):
    name = 'gumbel'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        thresh = kwargs.pop("thresh", 1.0)
        if thresh >= 1.1:
            raise ValueError("thresh must be less than 1.1")
        self.thresh = thresh

    def get_transform(self):
        return self.CustomTransform(self.thresh)

    def set_default_locators_and_formatters(self, axis):
        class DegreeFormatter(Formatter):
            def __call__(self, x, pos=None):
                # \u0025 : simbolo %
                return "%d%%" % (x * 0.02)
        axis.set_major_locator(FixedLocator(np.arange(0.0, 1.0, 0.02)))
        axis.set_major_formatter(DegreeFormatter())
        axis.set_minor_formatter(DegreeFormatter())

    class CustomTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            masked = ma.masked_where((a < -self.thresh) | (a > self.thresh), a)
            if masked.mask.any():
                return ma.exp(-np.exp(-a))
            else:
                return np.exp(-np.exp(-a))

        def inverted(self):
            return GumbelScale.InvertedCustomTransform(self.thresh)

    class InvertedCustomTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            return -np.log(-np.log(a))

        def inverted(self):
            return GumbelScale.CustomTransform(self.thresh)


mscale.register_scale(GumbelScale)

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    Datos = np.array([ 2690.0, 2700.0, 2700.667, 2701.333, 2702.0, 3196.0, 2372.0, 2395.0, 2128.0, 2727.0, 2431.0, 2850.0, 2216.0, 2057.0, 2269.0, 2208.0, 2628.0, 2729.0, 2588.0, 3448.0, 2508.0, 3081.0, 2417.0, 2770.0, 2283.0, 2455.0, 1963.0, 2786.0, 2885.0, 2357.0, 3422.0, 2423.0, 2148.0, 1305.0, 2472.0, 2186.0, 2720.0, 2430.0, 2304.0, 2556.0, 2625.0, 2164.0, 2585.0, ])
    DatosOrdenados = np.sort(Datos)
    mu = 2353.157
    sigma = 297.961
    from scipy.stats import gumbel_l
    rv = gumbel_l(5, scale=1)

    y1 = (DatosOrdenados - mu) / sigma
    x1 = np.exp(-np.exp(-y1))

    #y1 = (np.linspace(-10, 10, 1000) - rv.mean()) / rv.std()
    #x1 = np.exp(-np.exp(-y1))  #rv.cdf(y1)
    #y1 = y1 * x1.std() + x1.mean()

    plt.plot(x1, y1, 'ro', lw=2)
    plt.gca().set_xscale('gumbel')

    plt.xlabel('F(z)')
    plt.ylabel('z')
    plt.title('Papel de probabilidad de Gumbel')
    plt.xticks(rotation='vertical', fontsize=7)
    def form3(x, pos):
        return '%.3f' % x
    formatter = FuncFormatter(form3)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(formatter))
    plt.grid(True)

    plt.show()
