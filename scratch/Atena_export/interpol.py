from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

from matplotlib.colors import LinearSegmentedColormap, Colormap    

# my own colormap, similar to ATENA -- deafault = not used
cdict = {
    'red':   ( ( 0.0, 1.0, 1. ), ( 0.5, 0.0, 0.0 ), ( 1., 0., 0. ) ),
    'green': ( ( 0.0, 0.0, 0.0 ), ( 0.5, 1.0, 1.0 ), ( 1, 0, 0 ) ),
    'blue':  ( ( 0.0, 0.0, 0.0 ), ( 0.5, 0.0, 0.0 ), ( 1., 1.0, 0.5 ) )
    }
my_cmap_lin = LinearSegmentedColormap( 'my_colormap_lin', cdict, 256 )



# read export data
export = genfromtxt( 'export.txt', dtype='float', skip_header=1, delimiter=[11, 11, 11, 11, 11, 11, 11] )

# BEAM CUTS
# cut steel plates
y1 = 0.0
y2 = 0.5
mat1 = export[export[:, 1] > y1]
export = mat1[mat1[:, 1] < y2]

# cut beam in x-dirextion
#x1 = 0.0
#x2 = np.max( export[:, 0] )
#mat1 = export[export[:, 0] > x1]
#export = mat1[mat1[:, 0] < x2]


# npts -- number of points for new grid
npts = 1000
x = export[:, 0]
y = export[:, 1]
z = export[:, 2]
# define grid.
xi = np.linspace( np.min( export[:, 0] ), np.max( export[:, 0] ), npts )
# for concrete xi use
#xi = np.array( [0.06, 0.06] )
yi = np.linspace( np.min( export[:, 1] ), np.max( export[:, 1] ), npts )
# grid the data.
zi = griddata( x, y, z, xi, yi, interp='linear' ) # 'nn' = uses natural neighbor interpolation based on Delaunay triangulation

# ordinal number of x 1--npts in xi array
x_num = 10
# plot variable (e.g. stress) in cut
plt.plot( xi[x_num] + zi[:, x_num] / 10, yi, 'bo' )
print 'data of variable, e.g. stress', ' -- x-coordinate ', xi[x_num]
print zi[:, x_num]


# contour the gridded data, plotting dots at the nonuniform data points.
CS = plt.contour( xi, yi, zi, 25, linewidths=.5, colors='k' )
# plotting filled contour
CS = plt.contourf(xi, yi, zi, 25, cmap = my_cmap_lin) # my_cmap_lin , plt.cm.jet
plt.colorbar() # draw colorbar
# plot data integration points.
plt.scatter( x, y, marker='+', c='b', s=1, linewidth=.1 )


plt.xlim( -.5, .5 ) #np.min( export[:, 0] )   
plt.ylim( np.min( export[:, 1] ), np.max( export[:, 1] ) )     
plt.title( 'griddata test (%d points), cut in x=%.7f' % ( npts, xi[x_num] ) )
plt.show()



























# test case that scikits.delaunay fails on, but natgrid passes..
#data = np.array([[-1, -1], [-1, 0], [-1, 1],
#                 [ 0, -1], [ 0, 0], [ 0, 1],
#                 [ 1, -1 - np.finfo(np.float_).eps], [ 1, 0], [ 1, 1],
#                ])
#x = data[:,0]
#y = data[:,1]
#z = x*np.exp(-x**2-y**2)
## define grid.
#xi = np.linspace(-1.1,1.1,100)
#yi = np.linspace(-1.1,1.1,100)
## grid the data.
#zi = griddata(x,y,z,xi,yi)
