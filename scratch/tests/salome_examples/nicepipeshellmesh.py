#Copyright Open CASCADE 2007
#Author:      Sergey KUUL
#Description: This script is created for demonstration of
#             working MakePipeWithShellSection functionality
#             Using path and set of shell sections along it
#             pipe shape is created as set of solids. Each
#             result solid is a block. After that result
#             pipe shape is meshed by Hexahedron hypothesis


import geompy, smesh


#===========================================================
#    Auxilary functions for creation shell sections
#===========================================================

def MakeFaces(W1,W2):
    es1 = geompy.SubShapeAll(W1, geompy.ShapeType["EDGE"])
    es2 = geompy.SubShapeAll(W2, geompy.ShapeType["EDGE"])
    faces = []
    for i in range(0,8):
        e1 = es2[i]
        e3 = es1[i]
        ve1 = geompy.SubShapeAll(e1, geompy.ShapeType["VERTEX"])
        ve3 = geompy.SubShapeAll(e3, geompy.ShapeType["VERTEX"])
        e2 = geompy.MakeEdge(ve1[1],ve3[1])
        e4 = geompy.MakeEdge(ve3[0],ve1[0])
        w = geompy.MakeWire([e1,e2,e3,e4])
        f = geompy.MakeFace(w,1)
        faces.append(f)
        pass
    return faces


def MakeCircSect(v):
    c = geompy.PointCoordinates(v)
    W1 = geompy.MakeSketcher("Sketcher:F 10 0:R 90:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:WW",
                             [c[0], c[1], c[2], 1, 0, 0, 0, 0, 1])
    W1 = geompy.ChangeOrientation(W1)
    W2 = geompy.MakeSketcher("Sketcher:F 12 0:R 90:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:WW",
                             [c[0], c[1], c[2], 1, 0, 0, 0, 0, 1])
    faces = MakeFaces(W1,W2)
    shell = geompy.MakeSewing(faces,1.e-6)
    return shell


def MakeOvalSect1(v):
    c = geompy.PointCoordinates(v)
    W1 = geompy.MakeSketcher("Sketcher:F 23 0:R 90:C 8 90:T -15 0:T -15 0:R 0:C 8 90:R 0:C 8 90:T 15 0:T 15 0:R 0:C 8 90:WW",
                             [c[0], c[1], c[2], 1, 0, 0, 0, 1, 0])
    W1 = geompy.ChangeOrientation(W1)
    W2 = geompy.MakeSketcher("Sketcher:F 25 0:R 90:C 10 90:T -15 0:T -15 0:R 0:C 10 90:R 0:C 10 90:T 15 0:T 15 0:R 0:C 10 90:WW",
                             [c[0], c[1], c[2], 1, 0, 0, 0, 1, 0])
    faces = MakeFaces(W1,W2)
    shell = geompy.MakeSewing(faces,1.e-6)
    return shell


def MakeOvalSect2(v):
    c = geompy.PointCoordinates(v)
    W1 = geompy.MakeSketcher("Sketcher:F 35 0:R 90:C 15 90:T -20 0:T -20 0:R 0:C 15 90:R 0:C 15 90:T 20 0:T 20 0:R 0:C 15 90:WW",
                             [c[0], c[1], c[2], 1, 0, 0, 0, 1, 0])
    W1 = geompy.ChangeOrientation(W1)
    W2 = geompy.MakeSketcher("Sketcher:F 37 0:R 90:C 17 90:T -20 0:T -20 0:R 0:C 17 90:R 0:C 17 90:T 20 0:T 20 0:R 0:C 17 90:WW",
                             [c[0], c[1], c[2], 1, 0, 0, 0, 1, 0])
    faces = MakeFaces(W1,W2)
    shell = geompy.MakeSewing(faces,1.e-6)
    return shell


#=======================================================
#                 Create path for pipe
#=======================================================
WirePath = geompy.MakeSketcher("Sketcher:F 0 0:T 80 0:T 20 0:T 80 0:T 20 0:T 50 0:R 0:C 40 90:R 0:C -20 90:R 0:C -30 45:T 10 -10:R 0:C 20 45:T 50 0:T 20 0:T 100 0:T 20 0:R 0:C -20 45:R 0:C 20 45:T 40 0",
                               [0, 0, 0, 0, 0, 1, 1, 0, 0])
geompy.addToStudy(WirePath,"WirePath")

es = geompy.SubShapeAll(WirePath, geompy.ShapeType["EDGE"])
vs = geompy.SubShapeAll(WirePath, geompy.ShapeType["VERTEX"])


#=======================================================
#                 Create shell sections
#=======================================================
shells = []
subbases = []
locs = []

# 1 section
shell = MakeCircSect(vs[0])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[0])

# 2 section
shell = MakeCircSect(vs[1])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[1])

# 3 section
shell = MakeOvalSect1(vs[2])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[2])

# 4 section
shell = MakeOvalSect1(vs[3])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[3])

# 5 section
shell = MakeCircSect(vs[4])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[4])

# 6 section
shell = MakeCircSect(vs[5])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[5])

# 7 section
c = geompy.PointCoordinates(vs[6])
W1 = geompy.MakeSketcher("Sketcher:F 10 0:R 90:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:WW",
                         [c[0], c[1], c[2], 0, 1, 0, 0, 0, 1])
W1 = geompy.ChangeOrientation(W1)
W2 = geompy.MakeSketcher("Sketcher:F 12 0:R 90:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:WW",
                         [c[0], c[1], c[2], 0, 1, 0, 0, 0, 1])
faces = MakeFaces(W1,W2)
shell = geompy.MakeSewing(faces,1.e-6)
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[6])
locs.append(vs[6])

# 8 section
shell = MakeCircSect(vs[7])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[7])

# 9 section
c = geompy.PointCoordinates(vs[8])
W1 = geompy.MakeSketcher("Sketcher:F 10 0:R 90:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:WW",
                         [c[0], c[1], c[2], 1, -1, 0, 0, 0, 1])
W1 = geompy.ChangeOrientation(W1)
W2 = geompy.MakeSketcher("Sketcher:F 12 0:R 90:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:WW",
                         [c[0], c[1], c[2], 1, -1, 0, 0, 0, 1])
faces = MakeFaces(W1,W2)
shell = geompy.MakeSewing(faces,1.e-6)
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[8])

# 10 section
c = geompy.PointCoordinates(vs[9])
W1 = geompy.MakeSketcher("Sketcher:F 10 0:R 90:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:WW",
                         [c[0], c[1], c[2], 1, -1, 0, 0, 0, 1])
W1 = geompy.ChangeOrientation(W1)
W2 = geompy.MakeSketcher("Sketcher:F 12 0:R 90:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:WW",
                         [c[0], c[1], c[2], 1, -1, 0, 0, 0, 1])
faces = MakeFaces(W1,W2)
shell = geompy.MakeSewing(faces,1.e-6)
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[9])

# 11 section
shell = MakeCircSect(vs[10])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[10])

# 12 section
shell = MakeCircSect(vs[11])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[11])

# 13 section
shell = MakeOvalSect2(vs[12])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[12])

# 14 section
shell = MakeOvalSect2(vs[13])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[13])

# 15 section
shell = MakeCircSect(vs[14])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[14])

# 16 section
c = geompy.PointCoordinates(vs[15])
W1 = geompy.MakeSketcher("Sketcher:F 10 0:R 90:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:R 0:C 10 45:WW",
                         [c[0], c[1], c[2], 1, -1, 0, 0, 0, 1])
W1 = geompy.ChangeOrientation(W1)
W2 = geompy.MakeSketcher("Sketcher:F 12 0:R 90:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:R 0:C 12 45:WW",
                         [c[0], c[1], c[2], 1, -1, 0, 0, 0, 1])
faces = MakeFaces(W1,W2)
shell = geompy.MakeSewing(faces,1.e-6)
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[15])

# 17 section
shell = MakeCircSect(vs[16])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[16])

# 18 section
shell = MakeCircSect(vs[17])
shells.append(shell)
fs = geompy.SubShapeAllSorted(shell, geompy.ShapeType["FACE"])
subbases.append(fs[0])
locs.append(vs[17])

resc = geompy.MakeCompound(shells)
geompy.addToStudy(resc,"shells")
ress = geompy.MakeCompound(subbases)
geompy.addToStudy(ress,"subbases")
resl = geompy.MakeCompound(locs)
geompy.addToStudy(resl,"locs")


#===========================================================
#                   Create Pipe
#===========================================================

# Using pipe creation without selected subbases
subbases = []

Pipe = geompy.MakePipeWithShellSections(shells, subbases, locs, WirePath,
                                        theWithContact=0, theWithCorrection=0)
Pipe_id = geompy.addToStudy(Pipe,"Pipe")


#===========================================================
#             Preparation for meshing
#===========================================================

# find linear edges between sections before creation of mesh
# since it is needed to set for them  special 1D hypothesis
ex = []
ee = geompy.SubShapeAll(Pipe, geompy.ShapeType["EDGE"])
for e in ee:
    ve = geompy.SubShapeAll(e, geompy.ShapeType["VERTEX"])
    c1 = geompy.PointCoordinates(ve[0])
    c2 = geompy.PointCoordinates(ve[1])
    dd = (c2[1]-c1[1])*(c2[1]-c1[1]) + (c2[2]-c1[2])*(c2[2]-c1[2])
    if dd < 0.000001: ex.append(e)
    pass

ep = []
for e in ex:
    ve = geompy.SubShapeAll(e, geompy.ShapeType["VERTEX"])
    c1 = geompy.PointCoordinates(ve[0])
    c2 = geompy.PointCoordinates(ve[1])
    if (c2[0]-c1[0])*(c2[0]-c1[0]) < 0.0001: continue
    IsOnSection = 0
    for s in shells:
        vss = geompy.SubShapeAll(s, geompy.ShapeType["VERTEX"])
        nbp = 0
        for v in vss:
            c = geompy.PointCoordinates(v)
            dist = (c[0]-c1[0])*(c[0]-c1[0]) + (c[1]-c1[1])*(c[1]-c1[1]) + (c[2]-c1[2])*(c[2]-c1[2])
            if dist < 0.000001:
                nbp = nbp + 1
                break
            pass
        for v in vss:
            c = geompy.PointCoordinates(v)
            dist = (c[0]-c2[0])*(c[0]-c2[0]) + (c[1]-c2[1])*(c[1]-c2[1]) + (c[2]-c2[2])*(c[2]-c2[2])
            if dist < 0.000001:
                nbp = nbp + 1
                break
            pass
        if nbp==2:
            IsOnSection = 1
            break
        pass
        if nbp==1: break
        pass
    if IsOnSection == 0: ep.append(e)
    pass

gre = geompy.CreateGroup(Pipe,geompy.ShapeType["EDGE"])
geompy.UnionList(gre,ep)
geompy.addToStudyInFather(Pipe,gre,"gre")
if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)

#=======================================================
# Mesh creation:
# Wire discretisation; Nb.Segment=3
# Quadrangle(Mapping); Max.ElementArea=3
# Hexahedron

#Sub-mesh creation:
# Wire discretisation; LocalLength=10
#=======================================================

Mesh_1 = smesh.Mesh(Pipe)
Wire_discretisation = Mesh_1.Segment()
Nb_Segments = Wire_discretisation.NumberOfSegments(3)
Nb_Segments.SetDistrType( 0 )
Quadrangle_Mapping = Mesh_1.Quadrangle()
Hexahedron_i_j_k = Mesh_1.Hexahedron()
Mesh_1.Segment(gre).LocalLength(10)
if not Mesh_1.Compute():
    print 'Mesh computation failed!!!'

if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)
