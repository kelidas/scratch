'''
Created on 3.3.2010

@author: Vasek
'''
def Simulation():
    from traits.api import HasTraits, HasStrictTraits, Float, Property, cached_property, \
                                    Instance, List, on_trait_change, Int, Tuple, Bool, \
                                    DelegatesTo, Event, Enum, implements, Button, File, CFloat

    from traitsui.api import \
        View, Item, Tabbed, VGroup, HGroup, ModelView, HSplit, VSplit
    from traitsui.menu import OKButton
    from math import e, sqrt, log, pi, floor
    from matplotlib.figure import Figure
    from matplotlib.pyplot import plot, hist, show
    from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                        log as ln, append, logspace, hstack, sign, trapz, sin, cos, sqrt, \
                        ogrid, sort, nonzero, tanh, broadcast, ones_like, ones, arange, ndarray, diff, outer, \
                        copy, mean, exp, std, average, arctan, histogram2d, meshgrid, savetxt, transpose, var
    from pylab import savefig, plot, show, imshow, draw, colorbar, pcolor, subplot, title, legend
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

    def Heaviside( x ):
        return ( sign( x ) + 1.0 ) / 2.0



    # @todo: other types of crosssectional area
    def cut_area( df, lf, ss, phi, sec ):
        '''
            Solve area of cut fibers (elliptic crosssection)
        '''
        if ( 0 < phi < arctan( ( lf ) / df ) ) and ( ss - lf / 2. * cos( phi ) + df / 2. * sin( phi ) < sec < ss + lf / 2. * cos( phi ) - df / 2. * sin( phi ) ):
            return pi * df ** 2 / 4. / cos( phi )
        if ( phi == pi / 2. ) and ( ss - df / 2. < sec < ss + df / 2. ):
            return lf * sqrt( df ** 2 - 4 * abs( sx - sec ) ** 2 )
        if ( 0 < phi < arctan( ( lf ) / df ) ) and ( ss + lf / 2. * cos( phi ) - df / 2. * sin( phi ) < sec < ss + lf / 2. * cos( phi ) + df / 2. * sin( phi ) )and ( ss - lf / 2. * cos( phi ) - df / 2. * sin( phi ) < sec < ss - lf / 2. * cos( phi ) + df / 2. * sin( phi ) ):
            return 0
        else:
            return 0#df * lf / sin( phi )  
    cut_area_func = frompyfunc( cut_area, 5, 1 )

    def cut_fiber_distrib( L, l, phi ):
        if L >= 2 * l:
            return l * cos( phi ) * sin( phi ) / ( L - l * cos( phi ) ) / probability_cut_nooverlaps( L, l, 0 )
        #if phi > 0 and phi < arccos( L / l / 2. ): #L > l and L < 2 * l * cos( phi ):
        else:
            return ( l * cos( phi ) * sin( phi ) / ( L - l * cos( phi ) ) / probability_cut_nooverlaps( L, l, 0 ) ) * Heaviside( phi - arccos( L / 2. / l ) ) * Heaviside( pi / 2. - phi ) + sin( phi ) / probability_cut_nooverlaps( L, l, 0 ) * Heaviside( phi ) * Heaviside( arccos( L / 2. / l ) - phi )

    def le_sim( phi, x, lf ):
        '''
            Solve embedded length l_e of fiber
        '''
        return lf / 2. - abs( x ) / cos( phi )

    # @todo: very short specimen
    def le( L, l ):
        '''
            Solve embedded length l_e of fibes (including null values) (integral)
        '''
        if L < l:
            #print 'very short specimen',
            return L / 4.
        if L < 2. * l:
            #print 'short specimen',
            return - L / 4. - L / 4. * ln( L / 2. ) + L / 4. * ln( L ) + 1 / 2. * l * ( 1 - L / ( 2. * l ) ) + 1 / 4. * L * ln( L / ( 2. * l ) ) + l / 4.
        if L >= 2. * l:
            #print 'long specimen',
            return - 1 / 4. * l - 1 / 4. * L * ln( L - l ) + 1 / 4. * L * ln( L )









    # Configuration
    l_x = 0.1 # [m]
    l_y = 0.04 # [m]
    l_z = 0.04 # [m]
    vf = 0.015 # [-]
    lf = 0.017 # [m]
    df = 0.0003#0.175e-3 # [m]

    Ac = l_y * l_z
    Af = df ** 2 / 4. * pi
    print 'Area', Af
    n = int( Ac * l_x * vf / ( Af * lf ) )
    print 'number of fibers in specimen volume', n

    spec = Specimen( l_x = l_x, l_y = l_y, l_z = l_z )  #
    fib = Fibers( spec = spec, n = n, lf = lf, df = df, overlaps = True ) # #23e-6

    p = 1 / 2. * lf / l_x # probability_cut_nooverlaps( spec.l_x, fib.lf, 0. )
    #p = 1 / 2. * lf / l_x
    print 'probability', p
    bin_mean = fib.n * p
    bin_var = bin_mean * ( 1 - p )

    ek = bin_mean
    dk = bin_var
    std_k = sqrt( dk )
    print 'E[k] ', ek, 'D[k] ', dk, 'std', std_k, 'cov', std_k / ek

    ep_1 = 7.21819420846
    dp_1 = 17.3747024443
    std_p_1 = sqrt( dp_1 )
    print 'E[P1]', ep_1, 'D[P1]', dp_1, 'std', std_p_1, 'cov', std_p_1 / ep_1

    ep_k = ep_1 * ek
    dp_k = ek * dp_1 + dk * ep_1 ** 2
    std_p_k = sqrt( dp_k )
    print 'E[Pk]', ep_k, 'D[Pk]', dp_k, 'std', std_p_k, 'cov', std_p_k / ep_k
    print '#' * 50
    print 'E[P1]', ep_k, 'D[Pk]', dp_k, 'std', std_p_1 * sqrt( ek ), 'cov', std_p_1 * sqrt( ek ) / ep_k

    import matplotlib.pyplot as plt
    x = linspace( 0, ep_k + 3 * std_p_k, 1000 )
    #plt.plot( x, norm( ep_k, std_p_k ).pdf( x ) )




    n_sim = 100

    #sec = rand( 1, n_sec ) * l_x
    v = []

    # crosssectional position
    sec = .0 * spec.l_x / 2.#[-l_x * 0.99 / 2. , -l_x / 3., 0., l_x / 3. , l_x * 0.99 / 2. ]#linspace( 0, l_x, n_sec )

    E = 200.e9
    d = 0.0003
    A = d ** 2 * pi / 4.
    tau = 1.76e6 * d * pi
    f = 0.03
    def pullout2( w, le, phi ):
        w = w[None, :]
        le = le[:, None]
        phi = phi[:, None]
        d = sqrt( E * A * tau * w ) * exp( f * phi )
        p = ones_like( w ) * tau * le * exp( f * phi )
        return  d * Heaviside( p - d ) + p * Heaviside( d - p )
    p_plot = 0
    def cut_fibers():
        '''
            Plot cut fibers (only ellipses), solve mean value of area and embedded length of cut fibers.
            Plot histogram of embedded length.
        '''
        mask = matrix( fib.cut_func( sx, lx, sec ).astype( 'bool' ) )
        sx_cut = sx[ mask ]
        sy_cut = sy[ mask ]
        sz_cut = sz[ mask ]
        phi_x_cut = phi_x[ mask ]
        theta_cut = theta[ mask ]
        A_cut = sum( cut_area_func( fib.df, fib.lf, sx_cut, phi_x_cut, sec ) )
        le_cut = le_sim( phi_x_cut, abs( sx_cut - sec * ones_like( sx_cut ) ), fib.lf )
        le_cut_null = le_sim( phi_x, abs( sx - sec * ones_like( sx ) ), fib.lf ) * fib.cut_func( sx, lx, sec )
    #    fig6 = figure( 6 )
    #    ax6 = Axes( fig6, [.1, .1, .8, .8] )
    #    hist( le_cut, 50, normed=0 )
    #    #hist( le_cut_null[0], 50, normed=0 )
    #    title( 'Embedded length l_e' )
    #    figure( 8 )
    #    n_mask = 10
    #    title( 'Histograms of $\phi$ fraction = $\pi/%i$' % n_mask )
    #    for i in range( 0, n_mask ):
    #        mask1 = phi_x_cut > i * pi / 2. / n_mask
    #        mask2 = phi_x_cut < ( i + 1 ) * pi / 2. / n_mask
    #        pdf, bins, patches = hist( le_cut[mask1 * mask2], 50 , histtype='step', label='%i' % i )
    #        legend()
            #print mean( pdf )
    #    figure( 9 )
    #    title( 'Histogram of cut fibers angle' )
    #    xx = linspace( 0, pi / 2., 100 )
    #    hist( phi_x_cut, 50, normed=1 )
    #    plot( xx, sin( 2 * xx ), color='red', linewidth=4, label='overlaps' )
    #    plot( xx, cut_fiber_distrib( spec.l_x, fib.lf, xx ), color='green', linewidth=4, label='nooverlaps' )
    #    legend()

    #    fig10 = figure( 10 )
    #    title( '2D histogram of le and phi_x' )
    #    ax10 = Axes3D( fig10 )
    #    bin = 20
    #    H, xedges, yedges = histogram2d( le_cut, phi_x_cut, ( bin, bin ), normed=1 )    
    #    #extent = [xedges[0] * 100, xedges[-1] * 100, yedges[0], yedges[-1]] #[xedges[0], xedges[-1], yedges[0], yedges[-1]]
    #    #im = imshow( H )#'binary', cmap='jet' , extent=extent
    #    #im.set_interpolation( 'bilinear' )
    #    #colorbar()
    #    x = ( xedges[range( 0, len( xedges ) - 1 )] + xedges[range( 1, len( xedges ) )] ) / 2.
    #    y = ( yedges[range( 0, len( yedges ) - 1 )] + yedges[range( 1, len( yedges ) )] ) / 2.
    #    #ax10.scatter3D( xedges.ravel(), yedges.ravel(), H.ravel() )
    #    xx = outer( x, ones( len( y ) ) )
    #    yy = outer( ones( len( x ) ), y )
    #    z = outer( ones( len( y ) ), sin( 2 * y ) ) / fib.lf * 2# * probability_cut_nooverlaps( spec.l_x, fib.lf, 0 )#* fib.n
    #    zz = outer( ones( len( y ) ), cut_fiber_distrib( spec.l_x, fib.lf, y ) / fib.lf * 2 )
    #    ax10.plot_wireframe( xx, yy, H )#, rstride=1, cstride=1 
    #    ax10.plot_wireframe( xx, yy, z , color='red', label='overlaps' )
    #    ax10.plot_wireframe( xx, yy, zz , color='green', label='nooverlaps' )
    #    legend()

#        print '%%%%%%%%%%%%%%%%%%%'
#        print '%%Embedded length%%'
#        print '%%%%%%%%%%%%%%%%%%%'
#        print 'probability cut fibers', probability_cut_nooverlaps( spec.l_x, fib.lf, 0. )
#        print 'le_mean cut fibers (int/p) \t', le( spec.l_x, fib.lf ) / probability_cut_nooverlaps( spec.l_x, fib.lf, 0. )
#        print 'le_mean of cut fibers (sim) \t', mean( le_cut ), '\t |\t standard deviation \t', std( le_cut )
#        print 'include nulls (sim) \t\t', mean( le_cut_null )
#        print 'E[le] (int) \t\t\t', le( spec.l_x, fib.lf )
#        print 'cut fibers area', A_cut, 'Ac', spec._get_cross_area(), 'af', A_cut / spec._get_cross_area()*100, '%' 

        PP = tau * le_cut * e ** ( f * phi_x_cut )
        #print 'mean PP', mean( PP )      
        p_plot = pullout2( w, le_cut, phi_x_cut )
        P = mean( p_plot , axis = 0 )
        varP = var( pullout2( w, le_cut, phi_x_cut ), axis = 0 )
        #print 'mean P', P[-1], 'variance P', varP[-1]  
        return P, varP, p_plot

    P = []
    V = []
    w = linspace( 0, 0.016, 500 ) / 1000.
    for j in range( 0, n_sim ):
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
        vec_cut = fib.cut_func( sx, lx, sec )
        v.append( sum( vec_cut ) )
        pp, vv, pplt = cut_fibers()
        P.append( pp )
        V.append( vv )

    #plt.figure( 100 )
    #plt.plot( w, array( P ).T, color='red' )
    #plt.plot( w, mean( array( P ), axis=0 ), linewidth=3, color='blue' )
    print 'P', mean( P ), var( P ), std( P )



    p = probability_cut_nooverlaps( spec.l_x, fib.lf, sec )
    bin_mean = fib.n * p
    bin_stdv = sqrt( bin_mean * ( 1 - p ) )
    bin_skew = ( 1 - 2 * p ) / bin_stdv

    poiss_lambda = fib.n * p
    poiss_mean = poiss_lambda
    poiss_stdv = poiss_lambda ** ( 1 / 2. )
    poiss_skew = poiss_lambda ** ( -1 / 2. )

    # Volume fraction
    Vf = fib._get_volume()
    Vc = spec._get_volume()
    vol_frac_V = Vf / Vc * 100 * fib.n

    #vol_frac_A = mean( v_vol_frac_A ) / Ac * 100

    print "sec:", sec # , "vec ", v
    print "    mean value = %.5f" % ( matrix( v ).mean() ), "\t|  stnd devia = %.5f" % ( matrix( v ).std() )     , "\t|  skewness   ", skew( v )
    print "    mean_binom = %.5f" % bin_mean              , "\t|  stdv_binom = %.5f" % bin_stdv                   , "\t|  skew_binom ", bin_skew
    print "    mean_poiss = %.5f" % poiss_mean              , "\t|  stdv_poiss = %.5f" % poiss_stdv                   , "\t|  skew_poiss ", poiss_skew
    print "    vol_frac_V = %.3f%%" % vol_frac_V           # , "\t|  vol_frac_A = %.3g%%" % vol_frac_A                 , "\t|  v_V /  v_A ", vol_frac_V / vol_frac_A
    #print Af
    #print Af / cos_cut[cos_cut != 0]

    #for i in range( 0, len( cos_cut[0] ) ):
    #    if cos_cut[0][i] != 0:
    #        print cos_cut[0][i]
    return w, array( P ).T, mean( array( P ), axis = 0 ), array( V ).T, mean( array( V ), axis = 0 ), pplt







