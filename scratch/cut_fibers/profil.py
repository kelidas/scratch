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
from math import exp, e, sqrt, log, pi
from matplotlib.figure import Figure
from matplotlib.pyplot import plot, hist, show, legend
from numpy import array, linspace, frompyfunc, zeros, column_stack, \
                    log as ln, append, logspace, hstack, sign, trapz, sin, cos, \
                    ogrid, sort, ones_like, nonzero, ones, tanh, broadcast, ones_like, arange, ndarray, diff, minimum
from pylab import savefig, plot, show, title
from scipy.interpolate import interp1d
from scipy.optimize import brentq, newton
import scipy.interpolate
from scipy.stats import binom

from matplotlib.figure import Figure                       
from matplotlib.axes import Axes                           
from matplotlib.lines import Line2D                        
from matplotlib.backends.backend_agg import FigureCanvasAgg
 
from numpy.random import rand
from numpy import arccos, matrix, sum, arange

def Heaviside( x ):
    return ( sign( x ) + 1.0 ) / 2.0

sampling = 10000
lf = 1.
lc = 3.75

#n = 1 # we rotate one fiber
#n_spec = 100 # number of independent specimens (each of which is cut once and contains n fibers)
#nsim = 10000
#v = []
delta = linspace( -.5 * lf, .5 * lf, sampling )


vec_p3 = []
vec_p4 = []

for i in range( 0, len( delta ) ):
    p3 = ( -2. * delta[i] ** 2 + lf ** 2 ) / 2. / lf ** 2  
    p4 = ( 1. / 2. - delta[i] / lf ) * ln( ( lf + 2. * delta[i] ) / ( lf - 2. * delta[i] ) ) + ln( 2. * lf / ( lf + 2. * delta[i] ) )
    vec_p3.append( p3 )
    vec_p4.append( p4 )
    
    
    
def prob( lc, lf, delta ):
    #type I and III
    if ( lf <= lc / 2. - delta ) and ( lf <= lc / 2. + delta ):
        #print "Varianta I or III"
        return lc / lf * ( ln( lc / ( lc - lf ) ) ) - 1
    #type II
    if ( lf <= lc / 2. + delta ) and ( lf > lc / 2. - delta ):
        #print "Varianta II"
        return 1 / 2. / lf * ( ( lc + 2. * delta ) * ln( 2. / ( lc + 2. * delta ) ) - ( ln( lc - lf ) + 1 ) * ( lc - 2. * delta ) + 2. * lc * ln( lc ) ) 
    #type IV
    if ( lf > lc / 2. + delta ) and ( lf > lc / 2. - delta ):
        #print "Varianta IV"
        return  1 + 1 / lf * ( -lc + ( lc / 2. - delta ) * ln( ( lc + 2 * delta ) / ( lc - 2 * delta ) ) + lc * ln( 2 * lc / ( lc + 2 * delta ) ) ) 



delta_spec = linspace( 0, .5 * lc, sampling / 2 )

vec_spec_p4_I = []
vec_spec_p4_II = []
vec_spec_p4_IV = []
delta_I = []
delta_II = []
delta_IV = []

for i in range( 0, len( delta_spec ) ):
    #type I and III    
    if ( lf <= lc / 2. - delta_spec[i] ) and ( lf <= lc / 2. + delta_spec[i] ):
        vec_spec_p4_I.append( prob( lc, lf, delta_spec[i] ) )
        delta_I.append( delta_spec[i] )
    #type II
    if ( lf <= lc / 2. + delta_spec[i] ) and ( lf > lc / 2. - delta_spec[i] ):
        vec_spec_p4_II.append( prob( lc, lf, delta_spec[i] ) )
        delta_II.append( delta_spec[i] )
    #type IV
    if ( lf > lc / 2. + delta_spec[i] ) and ( lf > lc / 2. - delta_spec[i] ):
        vec_spec_p4_IV.append( prob( lc, lf, delta_spec[i] ) )
        delta_IV.append( delta_spec[i] )

area3 = trapz( y=vec_p3, x=delta )
area4 = trapz( y=vec_p4[1:-1], x=delta[1:-1] )

print "area 3 = ", area3
print "area 4 = ", area4
print "area 4 / area 3 = ", area4 / area3

#plot_delta_spec = hstack( ( delta_spec[::-1] * -1, delta_spec ) ) 
# plot_vec_spec_p4 = hstack( ( vec_spec_p4[::-1], vec_spec_p4 ) ) 
# area_spec_p4 = trapz( y=plot_vec_spec_p4[1:-1], x=plot_delta_spec[1:-1] )
# print "area_spec_p4 = ", area_spec_p4

# presah vlaken spec_3
vec_spec_p3_I = []
vec_spec_p3_II = []
delta_I_2 = []
delta_II_2 = []

def prob_2( lc, lf, delta ):
    #type I 
    if lf <= lc - 2. * delta:
        #print "Varianta I"
        return lf / lc / 2
    #type II
    if lf > lc - 2. * delta:
        #print "Varianta II"
        return 1 / 4. / lf / lc * ( lf ** 2 - 3 * lc ** 2 - 4 * delta * lf + 2 * lc * lf + 12 * lc * delta - 12 * delta ** 2 ) + ( lc - 2 * delta ) ** 2 / ( 2 * lf * lc )

for i in range( 0, len( delta_spec ) ):
    #type I    
    if lf <= lc - 2. * delta_spec[i]:
        vec_spec_p3_I.append( prob_2( lc, lf, delta_spec[i] ) )
        delta_I_2.append( delta_spec[i] )
    #type II
    if lf > lc - 2. * delta_spec[i]:
        vec_spec_p3_II.append( prob_2( lc, lf, delta_spec[i] ) )
        delta_II_2.append( delta_spec[i] )
    

# plot( delta, vec_p3, "r", delta, vec_p4, "b", plot_delta_spec, plot_vec_spec_p4, "g" )

plot( delta, vec_p3, "y", linewidth=.5 )
plot( delta, vec_p4, "c" , linewidth=.5 )
plot( delta_I  , vec_spec_p4_I  , "b-" , linewidth=3 )
plot( delta_II , vec_spec_p4_II , "r-" , linewidth=3 )
plot( delta_IV , vec_spec_p4_IV , "g-" , linewidth=3 )
plot( delta_I_2  , vec_spec_p3_I  , "m-" , linewidth=3 )
plot( delta_II_2 , vec_spec_p3_II , "k-" , linewidth=3 )
plot( [0, lc / 2.], [lf / lc / 2., lf / lc / 2.] )
legend( ( "p3", "p4", "I and III" , "II" , "IV", "p3_I", "p3_II" ) )
title( "Specimen: lc=%.2f, lf=%.2f" % ( lc, lf ) )
show()



# vypocet v miste podminek
lf = 1.
delta = 0.3
lc = 1.4 #( lf + delta ) * 2.
print lc / lf * ( ln( lc / ( lc - lf ) ) ) - 1
print 1 / 2. / lf * ( ( lc + 2. * delta ) * ln( 2. / ( lc + 2. * delta ) ) - ( ln( lc - lf ) + 1 ) * ( lc - 2. * delta ) + 2. * lc * ln( lc ) )
print 1 + 1 / lf * ( -lc + ( lc / 2. - delta ) * ln( ( lc + 2 * delta ) / ( lc - 2 * delta ) ) + lc * ln( 2 * lc / ( lc + 2 * delta ) ) )

