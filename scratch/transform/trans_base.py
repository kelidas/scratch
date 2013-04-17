import numpy as np
from scipy import linalg
from StringIO import StringIO



#load bars
input=open("bar.dat","r")
bar_data=input.read()
#bars = np.loadtxt('bar.dat', dtype='float', comments='#', delimiter='\t', skiprows=1)
bars = np.genfromtxt(StringIO(bar_data), comments='#',skip_header=1, delimiter="\t")
#print bars

#load nodes
input=open("node.dat","r")
node_data=input.read()
nodes = np.genfromtxt(StringIO(node_data), comments='#',skip_header=1, delimiter="\t")
#print nodes

#global coordinate system vectors xyz
x = np.mat([1., 0., 0.])
y = np.mat([0., 1., 0.])
z = np.mat([0., 0., 1.])

#local coordinate system XYZ
#vector of axis X
nx1 = 0.
ny1 = 0.
nz1 = 0.
nx2 = 1.
ny2 = 2.
nz2 = 3.
node1 = np.array([nx1, ny1, nz1])
node2 = np.array([nx2, ny2, nz2])

X = np.mat([nx2-nx1, ny2-ny1, nz2-nz1])

#vector Y, Y[0,2] will be 0
Y = np.mat([0., 0., 0.])
if X[0,1]>0:
    Y[0,0] = -1
elif X[0,1]==0:
    Y[0,0] = 0
else:
     Y[0,0] = 1

if X[0,1]==0:
    Y[0,1] = 1
else:
    Y[0,1] = -Y[0,0]*X[0,0]/X[0,1]

#vector Z
Z = np.cross(X,Y)

#axis cos(angle)
xX = x*X.T/(linalg.norm(x)*linalg.norm(X))
xY = x*Y.T/(linalg.norm(x)*linalg.norm(Y))
xZ = x*Z.T/(linalg.norm(x)*linalg.norm(Z))
yX = y*X.T/(linalg.norm(y)*linalg.norm(X))
yY = y*Y.T/(linalg.norm(y)*linalg.norm(Y))
yZ = y*Z.T/(linalg.norm(y)*linalg.norm(Z))
zX = z*X.T/(linalg.norm(z)*linalg.norm(X))
zY = z*Y.T/(linalg.norm(z)*linalg.norm(Y))
zZ = z*Z.T/(linalg.norm(z)*linalg.norm(Z))

#transformation matrix R (rotation)
R = np.mat([[xX[0,0], xY[0,0], xZ[0,0]],[yX[0,0], yY[0,0], yZ[0,0]],[zX[0,0], zY[0,0], zZ[0,0]]])

#transformation global v to local V
v = np.mat([-1,-5,-10]) #-10.96; 1.34; -2.03
V = R.T * v.T
#print V


print "hotovo"
