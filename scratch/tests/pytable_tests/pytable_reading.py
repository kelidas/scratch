'''
Created on Oct 15, 2010

@author: kelidas
'''
import tables

print tables.__version__

f = tables.openFile( "test.h5" )
print f.root
print f.root.detector.readout[1::3]
table = f.root.detector.readout
pressure = [ x['pressure'] for x in table.iterrows()
              if x['TDCcount'] > 3 and 20 <= x['pressure'] < 50 ]
print 'pressure', pressure

print 'energy', table.cols.energy[:]

print [row['energy'] for row in table.where( 'pressure > 10' )]


f.close()
