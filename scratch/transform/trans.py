#-*- coding: utf8 -*-
import numpy as np
from scipy import linalg
from StringIO import StringIO



#load bar data
input = open( "bar.dat", "r" )
bar_data = input.read()
#bars = np.loadtxt( 'bar.dat', dtype='float', comments='#', delimiter='\t', skiprows=1 )
bars = np.genfromtxt( StringIO( bar_data ), comments='#', skip_header=1, delimiter="\t" )
#print bars
input.close()

#load node data
input = open( "node.dat", "r" )
node_data = input.read()
nodes = np.genfromtxt( StringIO( node_data ), comments='#', skip_header=1, delimiter="\t" )
#print nodes  
input.close()

#load deformation data
input = open( "deform.dat", "r" )
deform_data = input.read()
deform = np.genfromtxt( StringIO( deform_data ),
                       dtype="i4,S25,float,float,float,float,float,float",
                       comments='#', skip_header=1, delimiter="\t" )
#print deform
input.close()

#global coordinate system vectors xyz
x = np.mat( [1., 0., 0.] )
y = np.mat( [0., 1., 0.] )
z = np.mat( [0., 0., 1.] )

output = open( "output.dat", "w" )
output.write( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % 
             ( "Node", "Load", "DX (mm)", "DY (mm)", "DZ (mm)", "RX ([rad])", "RY ([rad])", "RZ ([rad])" ) )

for i in range( 0, len( bars ) ):
    for j in range( 0, len( nodes ) ):
        #local coordinate system XYZ
        #vector of axis X
        if nodes[j, 0] == bars[i, 1]:
            node1 = np.array( [nodes[j, 1],
                              nodes[j, 2],
                              nodes[j, 3]] )
        if nodes[j, 0] == bars[i, 2]:
            node2 = np.array( [nodes[j, 1],
                              nodes[j, 2],
                              nodes[j, 3]] )

    X = np.mat( node2 - node1 )

    #vector Y, Y[0,2] will be 0
    Y = np.mat( [0., 0., 0.] )
    if X[0, 1] > 0:
        Y[0, 0] = -1
    elif X[0, 1] == 0:
        Y[0, 0] = 0
    else:
        Y[0, 0] = 1

    if X[0, 1] == 0:
        Y[0, 1] = 1
    else:
        Y[0, 1] = -Y[0, 0] * X[0, 0] / X[0, 1]

    #vector Z
    Z = np.cross( X, Y )


    #axis globLOC cos(angle)
    xX = x * X.T / ( linalg.norm( x ) * linalg.norm( X ) )
    xY = x * Y.T / ( linalg.norm( x ) * linalg.norm( Y ) )
    xZ = x * Z.T / ( linalg.norm( x ) * linalg.norm( Z ) )
    yX = y * X.T / ( linalg.norm( y ) * linalg.norm( X ) )
    yY = y * Y.T / ( linalg.norm( y ) * linalg.norm( Y ) )
    yZ = y * Z.T / ( linalg.norm( y ) * linalg.norm( Z ) )
    zX = z * X.T / ( linalg.norm( z ) * linalg.norm( X ) )
    zY = z * Y.T / ( linalg.norm( z ) * linalg.norm( Y ) )
    zZ = z * Z.T / ( linalg.norm( z ) * linalg.norm( Z ) )

    #transformation matrix R (rotation)
    R = np.mat( [[xX[0, 0], xY[0, 0], xZ[0, 0], 0, 0, 0],
                [yX[0, 0], yY[0, 0], yZ[0, 0], 0, 0, 0],
                [zX[0, 0], zY[0, 0], zZ[0, 0], 0, 0, 0],
                [0, 0, 0, xX[0, 0], xY[0, 0], xZ[0, 0]],
                [0, 0, 0, yX[0, 0], yY[0, 0], yZ[0, 0]],
                [0, 0, 0, zX[0, 0], zY[0, 0], zZ[0, 0]]] )

    #transformation global v to local V
    for k in range( 0, len( deform ) ):
        if deform[k][0] == bars[i, 1]:
            v_node1 = np.mat( [deform[k][2],
                              deform[k][3],
                              deform[k][4],
                              deform[k][5],
                              deform[k][6],
                              deform[k][7]] ) 
            V_node1 = R.T * v_node1.T
            output.write( "%i\t%s\t%.16e\t%.16e\t%.16e\t%.16e\t%.16e\t%.16e\n" % ( bars[i, 1], deform[k][1], V_node1[0], V_node1[1], V_node1[2], V_node1[3], V_node1[4], V_node1[5] ) )
        if deform[k][0] == bars[i, 2]:
            v_node2 = np.mat( [deform[k][2],
                              deform[k][3],
                              deform[k][4],
                              deform[k][5],
                              deform[k][6],
                              deform[k][7]] )
            V_node2 = R.T * v_node2.T
            output.write( "%i\t%s\t%.16e\t%.16e\t%.16e\t%.16e\t%.16e\t%.16e\n" % ( bars[i, 2], deform[k][1], V_node2[0], V_node2[1], V_node2[2], V_node2[3], V_node2[4], V_node2[5] ) )
    #print V_node1.T
    #output file write
  
output.close()

print "hotovo"
