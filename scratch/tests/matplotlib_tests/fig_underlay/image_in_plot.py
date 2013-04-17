'''
Created on Dec 1, 2010

@author: kelidas
'''




#!/usr/bin/env python
from numpy import arange, loadtxt
from pylab import *
try:
    import Image
except ImportError, exc:
    raise SystemExit( "PIL must be installed to run this example" )

PX2MUM = 1.2 / 2.005

data = loadtxt( 'cut11_cf.txt' )
data_raw = loadtxt( 'cut11_raw.txt' )

im = imread( 'V1bSchnitt11.jpg' )
extent = ( 0, im.shape[1] / PX2MUM, 0, im.shape[0] / PX2MUM )
ims = imshow( im, origin = 'upper', aspect = 'equal', extent = extent ) # , cmap=cm.hot, extent=extent )
scatter_x = data_raw[:, 0]
scatter_y = data_raw[:, 1]
scatter( scatter_x[scatter_x <= im.shape[1] / PX2MUM] + 0, scatter_y[scatter_x <= im.shape[1] / PX2MUM] - 250, s = 40, marker = 'x' )
#scatter( data_raw[:, 0] + 0, data_raw[:, 1] - 250, s = 40, marker = 'x' )
scat_x = data[:, 0]
scat_y = data[:, 1]
scat = scatter( scat_x[scat_x <= im.shape[1] / PX2MUM] + 0, scat_y[scat_x <= im.shape[1] / PX2MUM] - 250, s = 45, c = data[:, 2][scat_x <= im.shape[1] / PX2MUM] )
plt.colorbar( scat )
show()
















exit()

lena = Image.open( 'V1bSchnitt11.tif' )
dpi = rcParams[ 'figure.dpi' ] * 2 * 10
print dpi
figsize = lena.size[0] / dpi, lena.size[1] / dpi

figure( figsize = figsize )
ax = axes( [0.1, 0.1, .8, .8] )#, frameon=False )
#ax.set_axis_off()

ax.plot( [10, 400], [10, 400], 'ro-' )
im = imshow( lena, origin = 'lower' )

ax.set_xticks( arange( 0, 2000, 100 ) )


show()

















exit()

#!/usr/bin/env python
from pylab import *

w, h = 512, 512
s = file( 'ct.raw', 'rb' ).read()
A = fromstring( s, uint16 ).astype( float )
A *= 1.0 / max( A )
A.shape = w, h

subplot( 211 )
extent = ( 0, 25, 0, 25 )
im = imshow( A, cmap = cm.hot, origin = 'upper', extent = extent )

markers = [( 15.9, 14.5 ), ( 16.8, 15 )]
x, y = zip( *markers )
plot( x, y, 'o' )
#axis([0,25,0,25])



#axis('off')
title( 'CT density' )

from numpy import sum
x = sum( A, 0 )
subplot( 212 )
bar( arange( w ), x )
xlim( 0, h - 1 )
ylabel( 'density' )
setp( gca(), 'xticklabels', [] )

show()



exit()
