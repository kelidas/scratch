'''
Created on 3.3.2010

@author: Vasek
'''
from traitsui.toolkit import ETSConfig
ETSConfig.toolkit = 'qt4'
from traits.api import HasTraits, HasStrictTraits, Float, Property, cached_property, \
                                Instance, List, on_trait_change, Int, Tuple, Bool, \
                                DelegatesTo, Event, Enum, implements, Button, File, CFloat, Str, \
                                Array, Dict, Range

from traitsui.api import \
    View, Item, Tabbed, VGroup, HGroup, ModelView, HSplit, VSplit, RangeEditor
from traitsui.menu import OKButton
from math import exp, e, sqrt, log, pi
from matplotlib.figure import Figure
from matplotlib.pyplot import plot, hist, show
from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                    log as ln, append, logspace, hstack, sign, trapz, sin, cos, \
                    ogrid, sort, nonzero, tanh, broadcast, ones_like, arange, ndarray, diff
from pylab import savefig, plot, show
from scipy.interpolate import interp1d
from scipy.optimize import brentq, newton
import scipy.interpolate

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg

from numpy.random import rand
from numpy import arccos, matrix, sum, arange, memmap, mean, var

import matplotlib.pylab as plt

import time
from scipy import stats
from scipy.stats import uniform, norm, weibull_min

from scipy.optimize import fsolve

from traitsui.qt4.extra.bounds_editor import BoundsEditor
from enable.slider import Slider

class A(HasTraits):
    low = Int(0)  # Range(0, 'maxv', 0)
    high = Int(100)  # Range(0, 'maxv', 'maxv')
    value = Int
    v = Int(100)
    maxv = Int(100)

    def _value_changed(self):
        if self.value >= self.v:
            self.v = self.value + 1

    def _v_changed(self):
        if self.value >= self.v:
            self.value = self.v - 1

    views = View(Item('value',
                   editor=RangeEditor(low=0,
                                         high_name='high',
                                         format='%d',
                                         label_width=28,
                                         mode='auto')),
                Item('v',
                   editor=RangeEditor(low_name='low',
                                         high=100,
                                         format='%d',
                                         label_width=28,
                                         mode='auto')),
                )



class Foo(HasTraits):
    bounds = Range(10, 20, value=15, auto_set=True)
    incr_low = Button("incr_low")
    first = Float(10)
    second = Float(20)

    traits_view = View(Item('bounds', editor=BoundsEditor(low_name='first', high_name='second')),
                        Item('incr_low'))

    def _incr_low_changed(self):
        self.first += 1

    def _first_changed(self, old, new):
        print "new low:", new

        if self.first >= self.second:
            self.second = self.first + 5

Foo().configure_traits()


A().configure_traits()

exit()

# rv = getattr( stats, 'norm' )
rv = weibull_min(7.0544, loc=3.2925)
print rv.stats('m')

from traitsui.api import TextEditor
class Float_display(HasTraits):
    a = Float(0.1651651355646, editor=TextEditor(format_str='%.10f', auto_set=False, enter_set=True, evaluate=float))
    b = CFloat(5.2456165416516, editor=TextEditor(format_str='%.10f', auto_set=False, enter_set=True))
    c = Property(Float(0.0), depends_on='a', auto_set=False, enter_set=True)
    def _get_c(self):
        print self.a
        return self.a
    d = Property(Float(0.0), depends_on='b', readonly=True)
    def _get_d(self):
        print self.b
        return self.b
    def default_traits_view(self):
        view = View(VGroup(
                    Item('a', label='a') ,
                    Item('b', label='b') ,
                    Item('c', label='c', editor=TextEditor(format_str='%.3f')) ,
                    Item('d', label='d', editor=TextEditor(format_str='%.10f'))),
                    kind='live',
                    resizable=True,
                    id='pdistrib.distribution.view')
        return view

pok = Float_display()
pok.configure_traits()




exit()

def f(par):
    return par[0] ** 2 - par[1]

def func2(x):
        out = [x[0] * cos(x[1]) - 4]
        out.append(x[1] * x[0] - x[1] - 5)
        return out

print 'root', fsolve(f, [1., 2.])


x0 = 10.0
x2 = 0.0
init_val = [10, 20]

def DE_explicit_ss(s):
    sdot = zeros((2), 'd')
    sdot[0] = (10.0 * x0 - s[0]) - (5.0 * s[0] - s[1])
    sdot[1] = (5.0 * s[0] - s[1]) - (s[1] - x2)
    return sdot

sres = fsolve(DE_explicit_ss, init_val)

print 'result'
print sres


exit()
a = Arr()

a.configure_traits()

exit()
a = getattr(stats, 'uniform')
rvs = rand(100) * 10 + 5
print rvs
x = linspace(0, 20, 500)
plt.hist(rvs, 10 , normed=1)
loc, scale = tuple(a.fit(rvs, loc=mean(rvs), scale=sqrt(var(rvs))))
rv = uniform(loc=loc, scale=scale)
plt.plot(x, rv.pdf(x))
plt.show()

exit()

# plt.ion()
# for i in xrange( 0, 20 ):
#    plt.figure( 0 )
#    x = rand()
#    y = rand()
#    plt.plot( x, y, 'ro' )
#    plt.draw()
#    time.sleep( .1 )

# print 'ahoj'
# plt.show()
class A(HasStrictTraits):
    n = Float(2.)
    a = Property(depends_on='n')
    def _get_a(self):
        return 'a'

b = A()
print b.a

exit()
from numpy import asfarray
from scipy.optimize import anneal

# x_opt, retval = anneal( lambda x: ( 1 - sin( x ) / x ).sum(), asfarray( [-1, 1] ), T0=1, dwell=500 )
# print x_opt


import tables

class Inter(HasTraits):
    jmeno = Str('jmeno')
    def cislo(self):
        return 20

class Clovek(Inter):
    jmeno = Str('kuba')
    vek = Int(25)

class Zvire(Inter):
    rf = Instance(Clovek)
    jmeno = Str('punta')






# if __name__ == '__main__':
#    a.configure_traits()


exit()
plt.figure(0)


a = linspace(0, 100)
plt.plot(a, a)

plt.show()


exit()



def Heaviside(x):
    return (sign(x) + 1.0) / 2.0

def cut(sx, lx, x):
    if sx - lx / 2. < x < sx + lx / 2.:
        return 1
    else:
        return 0

func = frompyfunc(cut, 3, 1)

lf = 10
l_x = lf
l_y = 100
l_z = 30

n = 1
n_sec = 1000
x = 250

v = []
# lx = []
# sx = []
# sy = []
# cosO = []
# for i in range( 0, n_sec ):
#    cosO = 1 - rand( 1, n )
#    lx = lf * cosO
#    sx = l_x * rand( 1, n )
#    sy = l_y * rand( 1, n )
#    vec_cut = func( sx, lx, x )
#    v.append( sum( vec_cut ) )

#  varianta s vice vlakny
# cosO = 1 - rand( 1, n )
# lx = lf * cosO
# sx = l_x * rand( 1, n )
# sy = l_y * rand( 1, n )
# sec = rand( 1, n_sec ) * l_x
# for i in range( 0, n_sec ):
#    vec_cut = func( sx, lx, sec[0][i] )
#    v.append( sum( vec_cut ) )

for i in range(0, 10000):
    cosO = 1 - rand(1, n)
    lx = lf * cosO
    sx = l_x / 2.  # * rand( 1, n )
    # sy = l_y * rand( 1, n )
    # sec = rand( 1, n_sec ) * l_x
    sec = linspace(0, l_x, n_sec)
    vec_cut = 0
    for i in range(0, n_sec):
        vec_cut += func(sx, lx, sec[i])
    v.append(sum(vec_cut))
# print v


# plot figure of lx
# fig = Figure()  #figsize=[4, 4]
# ax = Axes( fig, [.1, .1, .8, .8] )
# fig.add_axes( ax )
# for i in range( 0, len( sx[0] ) ):
#    l = Line2D( [sx[0][i] - lf / 2. * cosO[0][i], sx[0][i] + lf / 2. * cosO[0][i]], [sy[0][i], sy[0][i]] )#- lf / 2. * sin( arccos( cosO[0][i] ) )
#    ax.add_line( l )
# ax.set_xlim( 0, 500 )
# ax.set_ylim( 0, 100 )
#
# canvas = FigureCanvasAgg( fig )
#
# canvas.print_figure( "line_ex.png" )

# plot histogram
pdf, bins, patches = hist(v, 1000, normed=0)  # , facecolor='green', alpha=1
# plot( sx, sy, 'rx' )   # centroids
# print sum( pdf * diff( bins ) )
show()
















print 'exit'
exit()


# a = Float( 10.0, pok='ahoj' )
#
# print a.__getattr__( 'pok' )
#
# class pok( HasTraits ):
#    b = Float( 10 )
#    c = CFloat( 3 )
#
#    def pod( self ):
#        return self.b / self.c
#
# d = pok()
# print d.pod()
#
# class Part( HasTraits ):
#    cost1 = Float( 0.0 )
#    cost2 = Float( 0.0 )
#
# class Widget( HasTraits ):
#    part1 = Instance( Part )
#    part2 = Instance( Part )
#    cost = Float( 0.0 )
#
#    def __init__( self ):
#        self.part1 = Part()
#        self.part2 = Part()
#        self.part1.on_trait_change( self.update_cost, 'cost1,cost2' )
#        self.part2.on_trait_change( self.update_cost, 'cost1,cost2' )
#
#    def update_cost( self ):
#        self.cost = self.part1.cost1 + self.part1.cost2 + self.part2.cost1 + self.part2.cost2
#
# w = Widget()
# w.part1.cost1 = 1
# print w.cost
# w.part1.cost2 = 2
# print w.cost
# w.part2.cost1 = 3
# print w.cost
# w.part2.cost2 = 4
# print w.cost
#
# from sympy import var, Plot
# x, y, z = var( 'x y z' )
# #Plot( x * y ** 3 - y * x ** 3 )

#
from scipy.weave import converters, inline
a = 5.
b = 6

code = """
    #line 79 "pok.py" (This is only useful for debugging)
    #ifdef _MSC_VER
    #define staticforward extern
    #endif

    return_val = a;
    """

err = inline(code, ['a'] , compiler='mingw32')
print 'asgsdfg', err




# def func( a ):
#    print a['a'] * 2
#
# dict = {'a':1, 'b':2}
# print dict.items()
# a, b = dict.values()
#
# lis = [5, 6, 3]
# for i, j in enumerate( dict ):
#    print i , j
#    lis[i] = dict[j]
# print 'list ', lis
#
# print str( dict )
#
# a = 1
# b = a
# b = 2
# print id( b ), id( a )
# print a


# for ii in dict:
#    vars()[str( ii )] = dict[ii]
# print a, b

# func( dict )

# strg = ''
# for ii in dict:
#    strg = strg + str( ii ) + '=' + str( dict[ii] ) + ','
#
#
# print 'f '
# eval( 'func(' + strg + ')' ), 'END'


# a = ogrid[0:1:20j]
# print a
#
# val = [ tt * 2. for tt in a ]
# print val
#
# dx = abs( a[0] - a[1] )
# print dx
#
# print sum( val ) * dx
# #print 1. * 2. / 2.
#


# a = ogrid[0:1:3j, 2:3:3j, 4:5:3j]
# for i in range( 0, 3 ):
#    print a[i]


# print a[0][1]
# print a[][]
# #val = [ tt * 2. for tt in a ]
# print sum( a[0].flatten() + a[1].flatten() + a[2].flatten() )*.1 * .1 * .1
#
# b = ogrid[0:1:3j, 0:1:3j]
# #val = [ tt * 2. for tt in a ]
# print b[0] + b[1]
# print sum( sum( b[0] + b[1] ) ) * .1 * .1

# print sum( sum( sum( a ) ) ) / 9.



# from numpy import array, argmin, sqrt, sum
# observation = array( [111.0, 188.0] )
# codes = array( [[102.0],
#      [132.0],
#    [45.0],
#     [57.0]] )
#
# diff = codes + observation
# dist = sqrt( sum( diff ** 2, axis= -1 ) )
# nearest = argmin( dist )
# print diff




# a = array( [ 1, 2, 3, 4, 5, 6] )
# print nonzero( a < 5 )


# class pokus( HasTraits ):
#    A = Float( 20., auto_set=False, Enter_set=True )
#    B = Float( 9., auto_set=False, Enter_set=True )
#
#
# if __name__ == '__main__':
#    p = pokus()
#    print 3 / p.B

exit()

a = ('0,' * 2 + '10,' * 77 + '20,' * 75 + '30,' * 47 + '40,' * 24 +
      '50,' * 16 + '60,' * 19 + '70,' * 20 + '80,' * 11 + '90,' * 15 +
      '100,' * 17 + '110,' * 12 + '120,' * 11 + '130,' * 11 + '140,' * 10 +
      '150,' * 10 + '160,' * 9 + '170,' * 9 + '180,' * 9 + '190,' * 13 +
      '200,' * 5 + '210,' * 7 + '220,' * 6 + '230,' * 10 + '240,' * 13 + '250,' * 12 +
      '260,' * 12 + '270,' * 10 + '280,' * 17 + '290,' * 27 + '300,' * 17 +
      '310,' * 13 + '320,' * 15 + '330,' * 37 + '340,' * 40 + '350,' * 56 +
      '360,' * 47 + '370,' * 42 + '380,' * 47 + '390,' * 32 + '400,' * 22 +
      '410,' * 20 + '420,' * 13 + '430,' * 11 + '440,' * 7 + '450,' * 5 +
      '460,' * 7 + '470,' * 3 + '480,' * 1 + '490,' * 3 + '500,' * 4 +
      '510,' * 2 + '520,' * 5 + '530,' * 3 + '540,' * 6 + '550,' * 5 + '560,' * 2 +
      '570,' * 2)

# print a

x = linspace(0, 570, 58)
y = array((2, 77, 75, 47, 24, 16, 19, 20, 11, 15, 17, 12, 11, 11, 10,
      10, 9, 9, 9, 13, 5, 7, 6, 10, 13, 12, 12, 10, 17, 27, 17,
      13, 15, 37, 40, 56, 47, 42, 47, 32, 22, 20, 13, 11, 7, 5,
      7, 3, 1, 3, 4, 2, 5, 3, 6, 5, 2, 2))
interpol = interp1d(x, y, kind='cubic')
newx = linspace(0, 570, 1000)
newy = interpol(newx)
print interpol.__dict__
plot(x, y, 'x', newx, newy, '-')
show()


exit()

# ##zahusteni grafu
x = linspace(0.0, 5.0, 11)

y1 = array([0., .5, 2., 3., 4., 5.])
y2 = array([5., 4.])
y3 = array([4., 4.5])
y4 = array([4.5, 3., 2., 1.5])
y = hstack([y1, y2, y3, y4])

x1 = x[:len(y1)]
x2 = x[len(y1) - 1 :len(y1) + len(y2) - 1 ]
x3 = x[len(y1) + len(y2) - 2 :len(y1) + len(y2) + len(y3) - 2]
x4 = x[len(y1) + len(y2) + len(y3) - 3:len(y1) + len(y2) + len(y3) + len(y4) - 3]

newx = linspace(0., 5., 24)
newy1 = linspace(0., y1[len(y1) - 1], 10)
newy2 = linspace(y2[0], y2[len(y2) - 1], 6)
newy3 = linspace(y3[0], y3[len(y3) - 1], 6)
newy4 = linspace(y4[0], y4[len(y4) - 1], 10)

lint1 = interp1d(y1, x1, kind='linear')
lint2 = interp1d(y2[::-1], x2[::-1], kind='linear', bounds_error=False)
lint3 = interp1d(y3, x3, kind='linear')
lint4 = interp1d(y4[::-1], x4[::-1], kind='linear')


newx1 = lint1(newy1)
newx2 = lint2(newy2[::-1])
newx3 = lint3(newy3)
newx4 = lint4(newy4[::-1])

plot(x1, y1, 'x', x2, y2, 'o', x3, y3, 'x', x4, y4, 'o', newx1, newy1, '.', \
      newx2[::-1], newy2, '.', newx3, newy3, '.', newx4[::-1], newy4, '.')
show()

# mint = interp1d( x, y, kind='linear', axis=1 )

# newx = linspace( 0, 5, 21 )
# newy = mint( newx )
# print newy

# plot( x, y, 'o', newx, newy, 'x' )
# show()


exit()


togrid = ogrid[ 0:1:5j, 0:1:5j, 0:1:5j ]
a = togrid[0]
b = togrid[1]
c = togrid[2]

eps_arr = linspace(0., 0.05, 70)

eps = eps_arr[:, None, None, None]
print eps




def Heaviside(x):
    return sign(sign(x) + 1)

Lf = 1.0

z = linspace(0.0, Lf / 2.0, 200)
phi = linspace(0.0, pi / 2.0, 200)

p_z = 2.0 / Lf
p_phi = sin(phi)

a_sum = sum(Heaviside(Lf / 2.0 - z / cos(phi)) * p_phi * p_z)
print 'sum ', a_sum  # * ( z[1] - z[2] ) * ( phi[1] - phi[2] )




def splitThousands(s, tSep=',', dSep='.'):
    '''Splits a general float on thousands. GIGO on general input'''
    if s == None:
        return 0
    if not isinstance(s, str):
        s = str(s)

    cnt = 0
    numChars = dSep + '0123456789'
    ls = len(s)
    while cnt < ls and s[cnt] not in numChars: cnt += 1

    lhs = s[ 0:cnt ]
    s = s[ cnt: ]
    if dSep == '':
        cnt = -1
    else:
        cnt = s.rfind(dSep)
    if cnt > 0:
        rhs = dSep + s[ cnt + 1: ]
        s = s[ :cnt ]
    else:
        rhs = ''

    splt = ''
    while s != '':
        splt = s[ -3: ] + tSep + splt
        s = s[ :-3 ]

    return lhs + splt[ :-1 ] + rhs

def mathFormat(s):
    '''Splits a general float on thousands. GIGO on general input'''
    # if s == None:
    #    return 0
    # if not isinstance( s, str ):
    #    s = str( s )
    if float(s) > 9999 or float(s) < -9999:
        dSep = '.'
        s = str(s)
        cnt = 0
        numChars = dSep + '0123456789'
        ls = len(s)
        while cnt < ls and s[cnt] not in numChars: cnt += 1

        lhs = s[ 0:cnt ]
        s = s[ cnt: ]
        if dSep == '':
            cnt = -1
        else:
            cnt = s.rfind(dSep)
        if cnt > 0:
            rhs = s[ cnt + 1: ]
            s = s[ :cnt ]
        else:
            rhs = ''

        expon = (len(s) - (len(s) % 3))
        splt = s[ 0:(len(s) - expon) ] + dSep + s[:len(s)]
        return lhs + splt + rhs + 'e' + str(expon)
    elif 1e-3 > float(s) > -1e-3:
        dSep = '.'
        s = str(s)
        cnt = 0
        numChars = dSep + '0123456789'
        ls = len(s)
        while cnt < ls and s[cnt] not in numChars: cnt += 1

        lhs = s[ 0:cnt ]
        s = s[ cnt: ]
        if dSep == '':
            cnt = -1
        else:
            cnt = s.rfind(dSep)
        if cnt > 0:
            rhs = s[ cnt + 1: ]
            s = s[ :cnt ]
        else:
            rhs = ''

        expon = (len(s) - (len(s) % 3))
        splt = s[ 0:(len(s) - expon) ] + dSep + s[:len(s)]
        return lhs + splt + rhs + 'e' + str(expon)




#####################################
if __name__ == "__main__" :
    def doIt(s):
        print "%s\t=>\t%s" % (s, mathFormat(s))

    for i in [0.1, .01, .0012, .000123, .000001234, .00000012345, -.000000123456, 1234567, 12345678, 123456789, -120000]:
        doIt(i)

    for i in [0, 1, 12, 123, 1234, 12345, 123456, 1234567, 12345678, 123456789, -120000]:
        doIt(i)

    mant = 0.987654321
    for i in [0, 1, 12, 123, 1234, 12345, 123456, 1234567, 12345678, 123456789]:
        doIt(str(i + mant))
        doIt(-1 * (i + mant))
