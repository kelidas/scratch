'''
Created on 3.3.2010

@author: Vasek
'''

from traits.api import HasTraits, HasStrictTraits, Float, Property, cached_property, \
                                Instance, List, on_trait_change, Int, Tuple, Bool, \
                                DelegatesTo, Event, Enum, implements, Button, File, CFloat

from traitsui.api import \
    View, Item, Tabbed, VGroup, HGroup, ModelView, HSplit, VSplit
from traitsui.menu import OKButton
from math import exp, e, sqrt, log, pi, floor
from matplotlib.figure import Figure
from matplotlib.pyplot import plot, hist, show, ylabel, xlabel, subplots_adjust
from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                    log as ln, append, logspace, hstack, sign, trapz, sin, cos, sqrt, \
                    ogrid, sort, nonzero, tanh, broadcast, ones_like, ones, arange, ndarray, diff, outer, \
                    copy, mean, std, average, arctan, histogram2d, meshgrid, savetxt, transpose, var
from pylab import savefig, plot, show, imshow, draw, colorbar, pcolor, subplot, title, legend, \
                xticks
from scipy.interpolate import interp1d
from scipy.optimize import brentq, newton
import scipy.interpolate

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_agg import FigureCanvasAgg

from numpy.random import rand
from numpy import arccos, matrix, sum, arange
from scipy.stats import binom, norm, skew, poisson

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D
from matplotlib.pyplot import figure

from specimen_3D.fibers import Fibers, Specimen
from specimen_3D.probability import probability_cut_nooverlaps
from mayavi.tools.helper_functions import plot3d

def Heaviside(x):
    return (sign(x) + 1.0) / 2.0



# @todo: other types of crosssectional area
def cut_area(df, lf, ss, phi, sec):
    '''
        Solve area of cut fibers (elliptic crosssection)
    '''
    # ellipse
    if (0 < phi < arctan((lf) / df)) and (ss - lf / 2. * cos(phi) + df / 2. * sin(phi) < sec < ss + lf / 2. * cos(phi) - df / 2. * sin(phi)):
        return pi * df ** 2 / 4. / cos(phi)
    # rectangular
    if (phi == pi / 2.) and (ss - df / 2. < sec < ss + df / 2.):
        return lf * sqrt(df ** 2 - 4 * abs(sx - sec) ** 2)
    if (0 < phi < arctan((lf) / df)) and (ss + lf / 2. * cos(phi) - df / 2. * sin(phi) < sec < ss + lf / 2. * cos(phi) + df / 2. * sin(phi))and (ss - lf / 2. * cos(phi) - df / 2. * sin(phi) < sec < ss - lf / 2. * cos(phi) + df / 2. * sin(phi)):
        pom = df / cos(phi)
        if pom > lf:
            pom = lf
            return df * pom
        else:
            return df * pom
    else:
        return 0#df * lf / sin( phi )  
cut_area_func = frompyfunc(cut_area, 5, 1)

def cut_fiber_distrib(L, l, phi):
    if L >= 2 * l:
        return l * cos(phi) * sin(phi) / (L - l * cos(phi)) / probability_cut_nooverlaps(L, l, 0)
    #if phi > 0 and phi < arccos( L / l / 2. ): #L > l and L < 2 * l * cos( phi ):
    else:
        return (l * cos(phi) * sin(phi) / (L - l * cos(phi)) / probability_cut_nooverlaps(L, l, 0)) * Heaviside(phi - arccos(L / 2. / l)) * Heaviside(pi / 2. - phi) + sin(phi) / probability_cut_nooverlaps(L, l, 0) * Heaviside(phi) * Heaviside(arccos(L / 2. / l) - phi)

def le_sim(phi, x, lf):
    '''
        Solve embedded length l_e of fiber
    '''
    return lf / 2. - abs(x) / cos(phi)

# @todo: very short specimen
def le(L, l):
    '''
        Solve embedded length l_e of fibes (including null values) (integral)
    '''
    if L < l:
        #print 'very short specimen',
        return L / 4.
    if L < 2. * l:
        #print 'short specimen',
        return -L / 4. - L / 4. * ln(L / 2.) + L / 4. * ln(L) + 1 / 2. * l * (1 - L / (2. * l)) + 1 / 4. * L * ln(L / (2. * l)) + l / 4.
    if L >= 2. * l:
        #print 'long specimen',
        return -1 / 4. * l - 1 / 4. * L * ln(L - l) + 1 / 4. * L * ln(L)









# Configuration
#spec = Specimen( l_x = 0.1, l_y = .04, l_z = .04 )  #
#fib = Fibers( spec = spec, n = 1997000, lf = .017, df = 0.0003, overlaps = True ) # #23e-6
spec = Specimen(l_x = 0.1, l_y = .04, l_z = .04)  #
fib = Fibers(spec = spec, n = 1000000, lf = .017, df = 0.0003, overlaps = False)

# number of histogram bins in cut_fibers()
nbins = 50

n_sim = 1

from matplotlib import rc, RcParams
rc('text', usetex = False)
rc('font', family = 'serif', serif = 'Times New Roman',
     style = 'normal', variant = 'normal', stretch = 'normal' , size = 16)
rc('legend', fontsize = 14)





print 'probability ', 1 / 2. * fib.lf / spec.l_x

#sec = rand( 1, n_sec ) * l_x
#
v = []
coef = []

# crosssectional position
sec = .0 * spec.l_x / 2.#[-l_x * 0.99 / 2. , -l_x / 3., 0., l_x / 3. , l_x * 0.99 / 2. ]#linspace( 0, l_x, n_sec )
sec = 0# 0.047

for j in range(0, n_sim):
    fib.sim_i = j
    sx = fib.sx
    lx = fib.lx
    sy = fib.sy
    ly = fib.ly
    sz = fib.sz
    lz = fib.lz
    phi_x = fib.phi_x
    theta = fib.theta
    phi_y = fib.phi_y
    phi_z = fib.phi_z
    vec_cut = fib.cut_func(sx, lx, sec)
    v.append(sum(vec_cut))
    #area = cut_area_func( fib.df, fib.lf, sx, phi_x, sec )
    #coef_ = area / ( pi * fib.df ** 2 / 4. )
    #coef.append( mean( coef_[coef_ > 0] ) )





#print 'number of cut fibers', v

p = probability_cut_nooverlaps(spec.l_x, fib.lf, sec)
bin_mean = fib.n * p
bin_stdv = sqrt(bin_mean * (1 - p))
bin_skew = (1 - 2 * p) / bin_stdv

poiss_lambda = fib.n * p
poiss_mean = poiss_lambda
poiss_stdv = poiss_lambda ** (1 / 2.)
poiss_skew = poiss_lambda ** (-1 / 2.)

# Volume fraction
Vf = fib._get_volume()
Vc = spec._get_volume()
vol_frac_V = Vf / Vc * 100 * fib.n

#vol_frac_A = mean( v_vol_frac_A ) / Ac * 100

print "sec:", sec # , "vec ", v
print "    mean value = %.5f" % (matrix(v).mean()), "\t|  stnd devia = %.5f" % (matrix(v).std())     , "\t|  skewness   ", skew(v)
print "    mean_binom = %.5f" % bin_mean              , "\t|  stdv_binom = %.5f" % bin_stdv                   , "\t|  skew_binom ", bin_skew
print "    mean_poiss = %.5f" % poiss_mean              , "\t|  stdv_poiss = %.5f" % poiss_stdv                   , "\t|  skew_poiss ", poiss_skew
print "    vol_frac_V = %.3f%%" % vol_frac_V           # , "\t|  vol_frac_A = %.3g%%" % vol_frac_A                 , "\t|  v_V /  v_A ", vol_frac_V / vol_frac_A
#print Af
#print Af / cos_cut[cos_cut != 0]

#for i in range( 0, len( cos_cut[0] ) ):
#    if cos_cut[0][i] != 0:
#        print cos_cut[0][i]

l_dict = { 'x':spec.l_x, 'y':spec.l_y, 'z':spec.l_z }
ss_dict = { 'x':sx, 'y':sy, 'z':sz }
def pdf_1d_I(xx, LL):
    return ln(LL / (LL - fib.lf)) / fib.lf

def pdf_1d_O(xx, LL):
    return ln(LL / (2 * xx)) / fib.lf

def pdf_1d(xx, par):
    LL = l_dict[par]
    def pdf_1d_val(xx, LL):
        if  0 < xx < LL / 2. - fib.lf / 2.:
            return  pdf_1d_I(xx, LL)
        if  LL / 2. - fib.lf / 2. < xx < LL / 2.:
            return pdf_1d_O(xx, LL)
    pdf_1d_func = frompyfunc(pdf_1d_val, 2, 1)
    #figure( 0 )
    #xx, yy = pdf_1d( xx, 'x' )
    #plot( xx, yy )
    return pdf_1d_func(xx, LL)


# 3D plot specimen with fibers
def fibers_3d():
    '''
        Plot fibers in 3D with matplotlib
    '''
    fig = figure(0)  #figsize=[4, 4] #Figure
    ax = Axes3D(fig, [.1, .1, .8, .8], azim = 90, elev = 90)

    fig.add_axes(ax)
    for i in range(0, len(sx[0])):
        l = Line3D([sx[0][i] - fib.lf / 2. * cos(phi_x[0][i]), sx[0][i] + fib.lf / 2. * cos(phi_x[0][i])], \
                     [sy[0][i] - fib.lf / 2. * cos(phi_y[0][i]), sy[0][i] + fib.lf / 2. * cos(phi_y[0][i])], \
                      [sz[0][i] - fib.lf / 2. * cos(phi_z[0][i]), sz[0][i] + fib.lf / 2. * cos(phi_z[0][i])], \
                      linewidth = .5)
        #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
        #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
        #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
        ax.add_line(l)

    ax.set_xlim3d(-spec.l_x / 2., spec.l_x / 2.)
    ax.set_ylim3d(-spec.l_y / 2., spec.l_y / 2.)
    ax.set_zlim3d(-spec.l_z / 2., spec.l_z / 2.)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    title('3D plot')




def fibers_2d_xy():
    '''
        Plot fibers in 2D section (plane XY)
    '''
    fig3 = figure(5)
    ax3 = Axes(fig3, [.1, .1, .8, .8])

    fig3.add_axes(ax3)
    for i in range(0, len(sx[0])):
        l = Line2D([sx[0][i] - fib.lf / 2. * cos(phi_x[0][i]), sx[0][i] + fib.lf / 2. * cos(phi_x[0][i])], \
                     [sy[0][i] - fib.lf / 2. * cos(phi_y[0][i]), sy[0][i] + fib.lf / 2. * cos(phi_y[0][i])], \
                      linewidth = .5, color = 'black')
        #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
        #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
        #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
        ax3.add_line(l)
    ax3.plot(sx, sy, 'ko', markersize = 3.0)
    ax3.plot([ -spec.l_x / 2., spec.l_x / 2. ], [spec.l_y / 2., spec.l_y / 2.], 'k-', linewidth = 2)
    ax3.plot([ -spec.l_x / 2., spec.l_x / 2. ], [-spec.l_y / 2., -spec.l_y / 2.], 'k-', linewidth = 2)
    ax3.plot([ spec.l_x / 2., spec.l_x / 2. ], [-spec.l_y / 2., spec.l_y / 2.], 'k-', linewidth = 2)
    ax3.plot([ -spec.l_x / 2., -spec.l_x / 2. ], [-spec.l_y / 2., spec.l_y / 2.], 'k-', linewidth = 2)
    ax3.set_axis_off()
    #ax3.set_xlim( -l_x / 2., l_x / 2. )
    #ax3.set_ylim( -l_y / 2., l_y / 2. )
    title('Fibers in 2D - xy')
    draw()

def fibers_2d_yz():
    '''
        Plot fibers in 2D section (plane YZ)
    '''
    fig2 = figure(1)
    ax2 = Axes(fig2, [.1, .1, .8, .8])

    fig2.add_axes(ax2)
    for i in range(0, len(sx[0])):
        l = Line2D([sy[0][i] - fib.lf / 2. * cos(phi_y[0][i]), sy[0][i] + fib.lf / 2. * cos(phi_y[0][i])], \
                      [sz[0][i] - fib.lf / 2. * cos(phi_z[0][i]), sz[0][i] + fib.lf / 2. * cos(phi_z[0][i])], \
                      linewidth = .5)
        #print  i, sx[0][i], lf / 2. * cosphi_x[0][i], [sx[0][i] - lf / 2. * cosphi_x[0][i], sx[0][i] + lf / 2. * cosphi_x[0][i]], \
        #             [sy[0][i] - lf / 2. * cosphi_y[0][i], sy[0][i] + lf / 2. * cosphi_y[0][i]], \
        #              [sz[0][i] - lf / 2. * cosphi_z[0][i], sz[0][i] + lf / 2. * cosphi_z[0][i]]                    
        ax2.add_line(l)
    ax2.plot(sy, sz, 'ro')
    ax2.plot([ -spec.l_y / 2., spec.l_y / 2. ], [spec.l_z / 2., spec.l_z / 2.], 'r-')
    ax2.plot([ -spec.l_y / 2., spec.l_y / 2. ], [-spec.l_z / 2., -spec.l_z / 2.], 'r-')
    ax2.plot([ spec.l_y / 2., spec.l_y / 2. ], [-spec.l_z / 2., spec.l_z / 2.], 'r-')
    ax2.plot([ -spec.l_y / 2., -spec.l_y / 2. ], [-spec.l_z / 2., spec.l_z / 2.], 'r-')
    #ax2.set_xlim( -l_y / 2., l_y / 2. )
    #ax2.set_ylim( -l_z / 2., l_z / 2. )
    title('Fibers in 2D - yz')
    draw()
    return 0


def cut_fibers():
    '''
        Plot cut fibers (only ellipses), solve mean value of area and embedded length of cut fibers.
        Plot histogram of embedded length.
    '''
    mask = matrix(fib.cut_func(sx, lx, sec).astype('bool'))
    sx_cut = sx[ mask ]
    sy_cut = sy[ mask ]
    sz_cut = sz[ mask ]
    phi_x_cut = phi_x[ mask ]
    theta_cut = theta[ mask ]
    def plot_cross_cut():
        #plot cut plane with crossection of cut fibers
        fig55 = figure(55)
        title('Cut fibers area (ellipses)')
        ax55 = Axes(fig55, [.1, .1, .8, .8])
        fig55.add_axes(ax55)
        for i in range(0, len(phi_x_cut)):
            sy_c = sy_cut[i] + (sec - sx_cut[i]) / cos(phi_x_cut[i]) * sin(phi_x_cut[i]) * cos(theta_cut[i])
            sz_c = sz_cut[i] + (sec - sx_cut[i]) / cos(phi_x_cut[i]) * sin(phi_x_cut[i]) * sin(theta_cut[i])
            if (0 < phi_x_cut[i] < arctan((fib.lf) / fib.df)) and (sx_cut[i] - fib.lf / 2. * cos(phi_x_cut[i]) + fib.df / 2. * sin(phi_x_cut[i]) < sec < sx_cut[i] + fib.lf / 2. * cos(phi_x_cut[i]) - fib.df / 2. * sin(phi_x_cut[i])):
                patch = Ellipse([ sy_c, sz_c ] , fib.df, fib.df / cos(phi_x_cut[i]), theta_cut[i] * 180 / pi , color = 'black')
                ax55.add_artist(patch)
        ax55.set_xlim(-spec.l_y / 2., spec.l_y / 2.)
        ax55.set_ylim(-spec.l_z / 2., spec.l_z / 2.)
    #plot_cross_cut() #plot cut plane
    A_cut = sum(cut_area_func(fib.df, fib.lf, sx_cut, phi_x_cut, sec))
    le_cut = le_sim(phi_x_cut, abs(sx_cut - sec * ones_like(sx_cut)), fib.lf)
    le_cut_null = le_sim(phi_x, abs(sx - sec * ones_like(sx)), fib.lf) * fib.cut_func(sx, lx, sec)
    fig6 = figure(6)
    ax6 = Axes(fig6, [.1, .1, .8, .8])
    hist(le_cut, nbins, normed = 0, color = '#cccccc')
    #hist( le_cut_null[0], 50, normed=0 )
    title('Embedded length l_e')
    figure(8)
    n_mask = 10
    title('Histograms of $\phi$ fraction = $\pi/%i$' % n_mask)
    for i in range(0, n_mask):
        mask1 = phi_x_cut > i * pi / 2. / n_mask
        mask2 = phi_x_cut < (i + 1) * pi / 2. / n_mask
        #pdf, bins, patches = hist( le_cut[mask1 * mask2], nbins , histtype = 'step', label = '%i' % i )
        legend()
        #print mean( pdf )
    figure(9)
    title('Histogram of cut fibers angle')
    xx = linspace(0, pi / 2., 100)
    hist(phi_x_cut, nbins, normed = 1, color = '#cccccc')
    if fib.overlaps:
        plot(xx, sin(2 * xx), color = 'k', linewidth = 4, label = 'overlaps')
        plot(xx, cut_fiber_distrib(spec.l_x, fib.lf, xx), 'k--', linewidth = 1, label = 'nooverlaps')
    else:
        plot(xx, sin(2 * xx), 'k--', linewidth = 1, label = 'overlaps')
        plot(xx, cut_fiber_distrib(spec.l_x, fib.lf, xx), color = 'k', linewidth = 4, label = 'nooverlaps')
    legend()

    fig10 = figure(10)
    title('2D histogram of le and phi_x')
    ax10 = Axes3D(fig10)
    bin = 20
    H, xedges, yedges = histogram2d(le_cut, phi_x_cut, (bin, bin), normed = 1)
    #extent = [xedges[0] * 100, xedges[-1] * 100, yedges[0], yedges[-1]] #[xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #im = imshow( H )#'binary', cmap='jet' , extent=extent
    #im.set_interpolation( 'bilinear' )
    #colorbar()
    x = (xedges[range(0, len(xedges) - 1)] + xedges[range(1, len(xedges))]) / 2.
    y = (yedges[range(0, len(yedges) - 1)] + yedges[range(1, len(yedges))]) / 2.
    #ax10.scatter3D( xedges.ravel(), yedges.ravel(), H.ravel() )
    xx = outer(x, ones(len(y)))
    yy = outer(ones(len(x)), y)
    z = outer(ones(len(y)), sin(2 * y)) / fib.lf * 2# * probability_cut_nooverlaps( spec.l_x, fib.lf, 0 )#* fib.n
    zz = outer(ones(len(y)), cut_fiber_distrib(spec.l_x, fib.lf, y) / fib.lf * 2)
    ax10.plot_wireframe(xx, yy, H)#, rstride=1, cstride=1 
    ax10.plot_wireframe(xx, yy, z , color = 'red', label = 'overlaps')
    ax10.plot_wireframe(xx, yy, zz , color = 'green', label = 'nooverlaps')
    legend()
    print '%%%%%%%%%%%%%%%%%%%'
    print '%%Embedded length%%'
    print '%%%%%%%%%%%%%%%%%%%'
    print 'probability cut fibers', probability_cut_nooverlaps(spec.l_x, fib.lf, 0.)
    print 'le_mean cut fibers (int/p) \t', le(spec.l_x, fib.lf) / probability_cut_nooverlaps(spec.l_x, fib.lf, 0.)
    print 'le_mean of cut fibers (sim) \t', mean(le_cut), '\t |\t standard deviation \t', std(le_cut)
    print 'include nulls (sim) \t\t', mean(le_cut_null)
    print 'E[le] (int) \t\t\t', le(spec.l_x, fib.lf)
    print 'cut fibers area', A_cut, 'Ac', spec._get_cross_area(), 'af', A_cut / spec._get_cross_area() * 100, '%'



def hist_f():
    '''
        Plot histograms of sx,sy,sz,phi_x,phi_y,phi_z in comparison with exact solution
    '''
    n_bin = 50
    xx = linspace(0, pi / 2., 100)
    fig7 = figure(7)
    subplot(231)
    hist(phi_x[0], n_bin, normed = 1)
    plot(xx, sin(xx), color = 'red', linewidth = 4)
    xx = linspace(0, pi, 100)
    subplot(232)
    hist(phi_y[0], n_bin, normed = 1)
    plot(xx, 1 / 2. * sin(xx), color = 'red', linewidth = 4)
    subplot(233)
    hist(phi_z[0], n_bin, normed = 1)
    plot(xx, 1 / 2. * sin(xx), color = 'red', linewidth = 4)
    subplot(234)
    xx = linspace(0, spec.l_x / 2., 100)
    hist(sx[0], n_bin, normed = 1)
    plot(xx, pdf_1d(xx, 'x'), color = 'red', linewidth = 4)
    subplot(235)
    xx = linspace(0, spec.l_y / 2., 100)
    hist(sy[0], n_bin, normed = 1)
    plot(xx, pdf_1d(xx, 'y'), color = 'red', linewidth = 4)
    subplot(236)
    xx = linspace(0, spec.l_z / 2., 100)
    hist(sz[0], n_bin, normed = 1)
    plot(xx, pdf_1d(xx, 'z'), color = 'red', linewidth = 4)







#canvas = FigureCanvasAgg( fig )    

#canvas.print_figure( "specimen3D.png" )   


# plot histogram
def fig2():
    '''
        Plot histogram and solve characteristics of probability_cut_nooverlapsability, that we cut fibers.
        Compare with binomial distribution.
        Set n_sim >> 1
    '''
    figure(2)
    subplots_adjust(wspace = 0., hspace = 0, bottom = .2)
    delta = 0.
    p = probability_cut_nooverlaps(spec.l_x, fib.lf, delta)
    # probability for extrusion
    #p = fib.lf / 2. / spec.l_x

    rvb = binom(fib.n, p)
    rvp = poisson(fib.n * p)
    rvn = norm(fib.n * p, sqrt(fib.n * p * (1 - p)))

    graph_from = floor(bin_mean - 4 * bin_stdv)
    graph_to = floor(bin_mean + 4 * bin_stdv) + 1


    x = arange(graph_from , graph_to)
    plot(x, n_sim * rvb.pmf(x), color = 'black', linestyle = '-', linewidth = 2, label = 'Binomial')
    plot(x, n_sim * rvp.pmf(x), color = 'black', linestyle = ':', linewidth = 1.5, label = 'Poisson')
    plot(x, n_sim * rvn.pdf(x), color = 'black', linestyle = '--', linewidth = 1.5, label = 'Normal')
    #plot( x, 20 * rv.pmf( x ) )

    pdf, bins, patches = hist(v, n_sim, normed = 0, facecolor = 'grey') #, alpha=1
    #set_xlim( bin_mean - 2 * bin_stdv, bin_mean + 2 * bin_stdv )
    #plot( sx, sy, 'rx' )   # centroids
    #print sum( pdf * diff( bins ) )
    xticks(position = (0, -0.01))
    xlabel('number of fibers')
    ylabel('frequency')
    legend()
    draw()


#print v
##for i in range( 0, len( v ) ): 
##    print v[i]
#print "mean value ", matrix( v ).mean(), "binom ", n * p
#print "standard deviation", matrix( v ).std(), "binom ", sqrt( n * p * ( 1 - p ) )
def pdf_x(L, l, delta, dv):
    if -L / 2 + l / 2 + dv < delta < L / 2 - l / 2 - dv:
        return 2 * dv / l * ln(L / (L - l))
    if  L / 2 - l / 2 - dv < delta < L / 2 - l / 2 + dv:
        return 1 / 2. + 1 / l * ((delta - dv) * ln(L - l) + (delta + dv) * (1 - ln(2 * (delta + dv))) + 2 * dv * ln(L) - L / 2.)
    if (delta > L / 2. - l / 2. + dv) and (delta > L / 2. - l / 2. - dv):
        return 1 / l * (2 * dv * (1 + ln(L / 2.)) - (delta + dv) * ln(delta + dv) + (delta - dv) * ln(delta - dv))
pdf_x_func = frompyfunc(pdf_x, 4, 1)

def pdf_x_0(L, l, delta, dv):
    if -L / 2 + l / 2 + dv < delta < L / 2 - l / 2 - dv:
        return 1 / l * ln(L / (L - l))
    if  L / 2 - l / 2 - dv < delta < L / 2 - l / 2 + dv:
        return 0
    if (delta > L / 2. - l / 2. + dv) and (delta > L / 2. - l / 2. - dv):
        return 1 / l * ln(L / (2 * delta))
pdf_x_0_func = frompyfunc(pdf_x_0, 4, 1)







def pdf_2d(par1, par2):
    LL1 = l_dict[par1]
    LL2 = l_dict[par2]
    xx = linspace(1e-6, LL1 / 2. - 1e-6, 100)
    yy = linspace(1e-6, LL2 / 2. - 1e-6, 100)
    xx, yy = meshgrid(xx, yy)
    def pdf_1d_val(xx, yy, LL1, LL2):
        if  (0 < xx < LL1 / 2. - fib.lf / 2.) and (0 < yy < LL2 / 2. - fib.lf / 2.):
            return  pdf_1d_I(xx, LL1) * pdf_1d_I(yy, LL2)
        if (0 < xx < LL1 / 2. - fib.lf / 2.) and (LL2 / 2. - fib.lf / 2. < yy < LL2 / 2.):
            return pdf_1d_I(xx, LL1) * pdf_1d_O(yy, LL2)
        if (LL1 / 2. - fib.lf / 2. < xx < LL1 / 2.) and (0 < yy < LL2 / 2. - fib.lf / 2.):
            return pdf_1d_O(xx, LL1) * pdf_1d_I(yy, LL2)
        if (LL1 / 2. - fib.lf / 2. < xx < LL1 / 2.) and (LL2 / 2. - fib.lf / 2. < yy < LL2 / 2.):
            return pdf_1d_O(xx, LL1) * pdf_1d_O(yy, LL2)
    pdf_1d_func = frompyfunc(pdf_1d_val, 4, 1)
    figure(1)
    xx, yy, zz = pdf_2d('x', 'z')
    pcolor(xx, yy , zz, cmap = 'jet')
    #im = imshow( zz, cmap='jet' )#, extent=extent
    colorbar()
    #im.set_interpolation( 'bilinear' )
    return xx, yy, pdf_1d_func(xx, yy, LL1, LL2)




def center_histogram_1d(par):
    '''
        Create histogram of fiber centroid in 1D and compare it with solved value
    '''
    fig33 = figure(3)
    ax33 = Axes(fig33, [.1, .1, .8, .8])
    fig33.add_axes(ax33)
    div = 100.
    ll = l_dict[par]
    ss = ss_dict[par]
    xx = linspace(0, ll / 2., 1000)
    #pdf, bins, patches = hist( sx[0], div, normed=0 )
    #plot( xx, pdf_x_func( l_x, lf, xx, l_x / div ) * n / 2., color='red', linewidth=4 )
    pdf, bins, patches = hist(ss[0], div, normed = 1)
    plot(xx, pdf_x_0_func(ll, fib.lf, xx, 0) , color = 'red', linewidth = 4)
    ax33.set_xticks(arange(-ll / 2., ll / 2., ll / 10.))
    title('histogram of fibers centroid in 1D -- sim')
    draw()


def center_histogram_2d(par1, par2):
    fig22 = figure(22)
    ax22 = Axes(fig22, [.1, .1, .8, .8])
    fig22.add_axes(ax22)
    div = 10.
    ll1 = l_dict[par1]
    ll2 = l_dict[par2]
    ss1 = ss_dict[par1]
    ss2 = ss_dict[par2]
    H, xedges, yedges = histogram2d(ss1[0], ss2[0], bins = [linspace(-ll1 / 2., ll1 / 2., div + 1) , linspace(-ll2 / 2., ll2 / 2., div * ll1 / ll2 + 1)], normed = 0)

    #extent = [-ll1 / 2., ll1 / 2., -ll2 / 2., ll2 / 2.]#[xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #im = imshow( H, extent=extent )#'binary', cmap='jet' 
    #im.set_interpolation( 'bilinear' )
    #colorbar()
    ax22 = Axes3D(fig22, [.1, .1, .8, .8])
    x = (xedges[range(0, len(xedges) - 1)] + xedges[range(1, len(xedges))]) / 2.
    y = (yedges[range(0, len(yedges) - 1)] + yedges[range(1, len(yedges))]) / 2.
    #ax10.scatter3D( xedges.ravel(), yedges.ravel(), H.ravel() )
    xx = outer(x, ones(len(y)))
    yy = outer(ones(len(x)), y)
    ax22.plot_wireframe(xx, yy, H)#, rstride=1, cstride=1 

    #H, xedges, yedges = histogram2d( ss1[0], ss2[0], bins=[div, div], normed=0 )
    #ax22.set_xticks( arange( -ll1 / 2., ll1 / 2., ll1 / 10. ) )
    #ax22.set_title( 'histogram of fibers centroid in 2D -- sim' )
    #ax22 = Axes3D( fig22 )
    #X, Y, Z = xedges, yedges, H
    #ax22.plot3D( X.ravel(), Y.ravel(), Z.ravel(), 'ro' )  
    #ax22.contour3D( X[:-1], Y[:-1], Z )
    #ax22.plot_wireframe( X, Y, Z, rstride=6, cstride=6, color='blue', linewidth=0.5 )
    #ax22.plot_surface( X[:-1], Y[:-1], Z )
    draw()
    return 0


def rhino_3d():
    '''
        Generate data for 3D model in Rhinoceros
    '''
#    A = [ sx - fib.lf / 2. * cos( phi_x ) - fib.df / 2. * sin( phi_x ), \
#         sy + ( fib.lf / 2. * sin( phi_x ) - fib.df / 2. * cos( phi_x ) ) * ( 2 * sin( theta / 2 ) * cos( theta / 2 ) ), \
#         sz - ( fib.lf / 2. * sin( phi_x ) - fib.df / 2. * cos( phi_x ) ) * ( 1 - 2 * sin( theta / 2 ) ** 2 ) ]
    A = [ sx - fib.lf / 2. * cos(phi_x) - fib.df / 2. * sin(phi_x), \
         sy + (fib.lf / 2. * sin(phi_x) - fib.df / 2. * cos(phi_x)) * (2 * sin(theta / 2) * cos(theta / 2)), \
         sz - (fib.lf / 2. * sin(phi_x) - fib.df / 2. * cos(phi_x)) * (1 - 2 * sin(theta / 2) ** 2) ]
#    B = [ sx - fib.lf / 2. * cos( phi_x ) + fib.df / 2. * sin( phi_x ), \
#         sy + ( fib.lf / 2. * sin( phi_x ) + fib.df / 2. * cos( phi_x ) ) * ( 2 * sin( theta / 2 ) * cos( theta / 2 ) ), \
#         sz - ( fib.lf / 2. * sin( phi_x ) + fib.df / 2. * cos( phi_x ) ) * ( 1 - 2 * sin( theta / 2 ) ** 2 ) ]
    B = [ sx - fib.lf / 2. * cos(phi_x) + fib.df / 2. * sin(phi_x), \
         sy + (fib.lf / 2. * sin(phi_x) + fib.df / 2. * cos(phi_x)) * (2 * sin(theta / 2) * cos(theta / 2)), \
         sz - (fib.lf / 2. * sin(phi_x) + fib.df / 2. * cos(phi_x)) * (1 - 2 * sin(theta / 2) ** 2) ]
    C = [ sx, sy, sz]#sx + fib.lf / 2. * cos( phi_x ), \
            #sy - ( fib.lf / 2. * sin( phi_x ) ) * ( 2 * sin( phi_x ) * cos( phi_x ) ), \
            #sz + ( fib.lf / 2. * sin( phi_x ) ) * ( 1 - 2 * sin( phi_x ) ** 2 ) ]
    ABC = array([ (A[0][0] + B[0][0]) / 2., (A[1][0] + B[1][0]) / 2., (A[2][0] + B[2][0]) / 2., \
                   C[0][0], C[1][0], C[2][0], \
                    0. * ones_like(sx)[0], 0. * ones_like(sy)[0], 0. * ones_like(sz)[0], \
                     0. * ones_like(sx)[0], fib.df / 2. * ones_like(sy)[0], 0. * ones_like(sx)[0], \
                     0. * ones_like(sx)[0], 0. * ones_like(sx)[0], fib.lf * ones_like(sz)[0]]) * 1000
    return savetxt('rhino_3d.dat', ABC.T)

def cut_area_coef():
    figure(33)
    hist(coef, nbins, normed = 0, facecolor = 'grey')

#fig2()
#rhino_3d()
cut_fibers()
#hist_f()
#fibers_2d_xy()
#fibers_2d_yz()
#center_histogram_1d( 'x' )
#center_histogram_2d( 'x', 'z' )
#fibers_3d()
#cut_area_coef()
show()









