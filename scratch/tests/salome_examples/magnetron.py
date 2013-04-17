#Copuright Open CASCADE 2007
#Author:      Sergey KUUL
#Description: This script is created for demonstration of
#             possibility of MeshEditor.
#             Part of magnetron is created using various
#             methods of MeshEditor.


import smesh, math

m = smesh.Mesh(0,"Mesh")
mesh = m.GetMesh()

e = mesh.GetMeshEditor()

# number of segments on 1/6 part of disk
ns = 10
# number of segments on full disk
nsc = 6*ns

# creation elements for external circle
# create section face
e.AddNode(222,0,10)
e.AddNode(178,0,10)
e.AddNode(178,0,-10)
e.AddNode(222,0,-10)
f1 = e.AddFace([1,2,3,4])
# and perform RotationSweep
axisZ = smesh.SMESH.AxisStruct( 0,0,0,0,0,1 )
e.RotationSweep([f1], axisZ, math.pi*2/nsc, nsc, 0.001)

# other elements will be created for 1/6 part of circle
# and after that (using hexa symmetry of shape) other
# elements will be created using method Rotate()

# creation parts of internal disks
r1 = 10
r2 = 60
r3 = 70
r4 = 15

zd1 = 40
zd2 = 48
zd3 = 56
zd4 = 63

vols = [] # list for all created elements
# 1 disk
ang = -math.pi/6
dang = math.pi/3/ns
x1 = r1*math.cos(ang)
y1 = r1*math.sin(ang)
x3 = r2*math.cos(ang)
y3 = r2*math.sin(ang)
n1 = e.AddNode(x1,y1,zd2)
n2 = e.AddNode(x1,y1,zd1)
n3 = e.AddNode(x3,y3,zd1)
n4 = e.AddNode(x3,y3,zd2)
dy = 2*r1*math.sin(math.pi/6)/ns
for i in range(1,11):
    y1 = y1 + dy
    x4 = r2*math.cos(ang + dang)
    y4 = r2*math.sin(ang + dang)
    n5 = e.AddNode(x1,y1,zd2)
    n6 = e.AddNode(x1,y1,zd1)
    n7 = e.AddNode(x4,y4,zd1)
    n8 = e.AddNode(x4,y4,zd2)
    nv = e.AddVolume([n1,n2,n3,n4,n5,n6,n7,n8])
    vols.append(nv)
    n1 = n5
    n2 = n6
    n3 = n7
    n4 = n8
    ang = ang + dang
    pass
    
# 2 disk
ang = -math.pi/6
x1 = r1*math.cos(ang)
y1 = r1*math.sin(ang)
x3 = r3*math.cos(ang)
y3 = r3*math.sin(ang)
n1 = e.AddNode(x1,y1,zd3)
n2 = e.AddNode(x1,y1,zd2)
n3 = e.AddNode(x3,y3,zd2)
n4 = e.AddNode(x3,y3,zd3)
dy = 2*r1*math.sin(math.pi/6)/ns
for i in range(1,11):
    y1 = y1 + dy
    x4 = r3*math.cos(ang + dang)
    y4 = r3*math.sin(ang + dang)
    n5 = e.AddNode(x1,y1,zd3)
    n6 = e.AddNode(x1,y1,zd2)
    n7 = e.AddNode(x4,y4,zd2)
    n8 = e.AddNode(x4,y4,zd3)
    nv = e.AddVolume([n1,n2,n3,n4,n5,n6,n7,n8])
    vols.append(nv)
    n1 = n5
    n2 = n6
    n3 = n7
    n4 = n8
    ang = ang + dang
    pass
    
# 3 disk
ang = -math.pi/6
x1 = r1*math.cos(ang)
y1 = r1*math.sin(ang)
x3 = r4*math.cos(ang)
y3 = r4*math.sin(ang)
n1 = e.AddNode(x1,y1,zd4)
n2 = e.AddNode(x1,y1,zd3)
n3 = e.AddNode(x3,y3,zd3)
n4 = e.AddNode(x3,y3,zd4)
dy = 2*r1*math.sin(math.pi/6)/ns
for i in range(1,11):
    y1 = y1 + dy
    x4 = r4*math.cos(ang + dang)
    y4 = r4*math.sin(ang + dang)
    n5 = e.AddNode(x1,y1,zd4)
    n6 = e.AddNode(x1,y1,zd3)
    n7 = e.AddNode(x4,y4,zd3)
    n8 = e.AddNode(x4,y4,zd4)
    nv = e.AddVolume([n1,n2,n3,n4,n5,n6,n7,n8])
    vols.append(nv)
    n1 = n5
    n2 = n6
    n3 = n7
    n4 = n8
    ang = ang + dang
    pass
    
# create U-link between external and internal circles
nb = 20
dx = 16
rr = (200+dx)/2
ri = rr - 2*dx
x1 = rr + rr*math.cos( math.pi*2/nsc*nb )
x2 = rr + ri*math.cos( math.pi*2/nsc*nb )
z1 = 10 + rr*math.sin( math.pi*2/nsc*nb )
z2 = 10 + ri*math.sin( math.pi*2/nsc*nb )
dy = x1*math.tan( math.pi/6 )

# create section face
n1 = e.AddNode(200+dx,dy,10)
n2 = e.AddNode(200-dx,dy,10)
n3 = e.AddNode(200-dx,-dy,10)
n4 = e.AddNode(200+dx,-dy,10)
axis1 = smesh.SMESH.AxisStruct( rr,0,10,0,-1,0 )
f1 = e.AddFace([n1,n2,n3,n4])
# and perform RotationSweep
e.RotationSweep([f1], axis1, math.pi*2/nsc, nb, 0.001)
newelems = e.GetLastCreatedElems()

# create other elements, wich connect U-link and
# internal disk
dang1 = math.acos((rr-x1)/ri)
dang1 = math.pi - dang1
dang2 = math.pi*2/nsc*nb
dang = (dang1+dang2)/2

x3 = rr + ri*math.cos(dang1)
z3 = 10 + ri*math.sin(dang1)
x4 = rr + ri*math.cos(dang)
z4 = 10 + ri*math.sin(dang)

n1 = e.AddNode(x1,dy,z1)
n2 = e.AddNode(x2,dy,z2)
n3 = e.AddNode(x3,dy,z3)
n4 = e.AddNode(x4,dy,z4)
n5 = e.AddNode(x1,-dy,z1)
n6 = e.AddNode(x2,-dy,z2)
n7 = e.AddNode(x3,-dy,z3)
n8 = e.AddNode(x4,-dy,z4)
vv = e.AddVolume([n1,n2,n4,n3,n5,n6,n8,n7])
vols.append(vv)

n3 = e.AddNode(x3,dy,zd3)
n7 = e.AddNode(x3,-dy,zd3)
x4 = 22*math.cos(math.pi/6)
y4 = 22*math.sin(math.pi/6)
n2 = e.AddNode(x4,y4,zd3)
n6 = e.AddNode(x4,-y4,zd3)
vv = e.AddVolume([n1,n3,n2,n5,n7,n6])
vols.append(vv)

# create other symmetric elements using method Rotate()
for i in range(1,6):
    e.Rotate(vols,axisZ,math.pi/3*i,1)
    e.Rotate(newelems,axisZ,math.pi/3*i,1)

if smesh.geompy.salome.sg.hasDesktop():
    smesh.geompy.salome.sg.updateObjBrowser(1)
