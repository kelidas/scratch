#Copyright Open CASCADE 2007
#Author Edward Agapov
#Example of mesh pattern mapping to convert triangles to set of quadrangles

import geompy, smesh
import os

######################################################################

def getTriaPattern(mesh):
    "Return loaded pattern mapper to split a triangle into 3 quadrangles"
    import math
    angle = 2 * math.pi / 3.
    x = math.cos( angle )
    y = math.sin( angle )
    midX = 0.5 * (1.0 + x)
    midY = 0.5 * y
    center = "0.0 0.0"
    p1     = "1.0 0.0"
    p2     = str( x )+" "+str( y )
    p3     = str( x )+" "+str(-y )
    mid1   = str( midX )+" "+str( midY )
    mid2   = str( x )+" 0.0"
    mid3   = str( midX )+" "+str(-midY )
    ##
    pattern = "\
    !!! Nb of points: \n 7 \n\
    !!! Points: \n "   + \
    center + " ! 0 \n " + \
    p1     + " ! 1 \n " + \
    p2     + " ! 2 \n " + \
    p3     + " ! 3 \n " + \
    mid1   + " ! 4 \n " + \
    mid2   + " ! 5 \n " + \
    mid3   + " ! 6 \n " + \
    "!!! Indices of key-points: \n\
    1 2 3 !!! p1, p2 and p3 \n\
    !!! Indices of points of 3 quadrangles: \n\
    1 4 0 6 \n\
    2 5 0 4 \n\
    3 6 0 5 \n"
    ##
    mapper = smesh.smesh.GetPattern()
    mapper.LoadFromFile(pattern)
    return mapper
    
######################################################################

def getQuadPattern(mesh):
    "Return loaded pattern mapper to split a quadrangle into quarters"
    pattern = "\
    !!! Nb of points: \n 9 \n\
    !!! Points: \n\
    0 0  !- 0 \n\
    1 0  !- 1 \n\
    2 0  !- 2 \n\
    0 1  !- 3 \n\
    1 1  !- 4 \n\
    2 1  !- 5 \n\
    0 2  !- 6 \n\
    1 2  !- 7 \n\
    2 2  !- 8 \n\
    !!! Indices of key-points: \n\
    0 2 6 8 \n\
    !!! Indices of points of 4 quadrangles: \n\
    0 1 4 3 \n\
    1 2 5 4 \n\
    3 4 7 6 \n\
    4 5 8 7 \n"
    ##
    mapper = smesh.smesh.GetPattern()
    mapper.LoadFromFile(pattern)
    return mapper

dir="/dn20/salome/eap/salome/misc/BREP/"
fileName = os.path.join( dir, "boat.brep" )

Shape_imp = geompy.ImportBREP(fileName)
if Shape_imp is None : 
    raise RuntimeError, "Can't import" + fileName

geompy.addToStudy( Shape_imp, "boat")  
if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)

######################################################################
# Meshing
# Wire discretisation; AverageLength=200
# Quadrangle(Mapping); QuadranglePreference
######################################################################

Mesh_1 = smesh.Mesh(Shape_imp, "Boat")
Wire_discretisation = Mesh_1.Segment()
hypNbSeg = Wire_discretisation.LocalLength(200)
smesh.SetName(hypNbSeg, "AverageLength_200")

Quadrangle_Mapping = Mesh_1.Quadrangle()
Quadrangle_Mapping.QuadranglePreference()

isDone = Mesh_1.Compute()
if not isDone:
    print 'Mesh computation failed!!!'
else:
    print "Information about the Boat mesh:"
    print "Number of nodes      : ", Mesh_1.GetMesh().NbNodes()
    print "Number of edges      : ", Mesh_1.GetMesh().NbEdges()
    print "Number of triangles  : ", Mesh_1.GetMesh().NbTriangles()
    print "Number of quadrangles: ", Mesh_1.GetMesh().NbQuadrangles()

    # merge coincident nodes to transform degenerated quads into triangles
    tol = 1e-5
    mesh_editor_0 = Mesh_1.GetMeshEditor()
    coincident_nodes = mesh_editor_0.FindCoincidentNodes( tol )
    mesh_editor_0.MergeNodes(coincident_nodes)
    
    faces = Mesh_1.GetElementsByType( smesh.SMESH.FACE )
    
    # refine quadrangles
    quad_pattern = getQuadPattern(Mesh_1)
    quad_pattern.ApplyToMeshFaces( Mesh_1.GetMesh(), faces, 1, False)
    quad_pattern.MakeMesh( Mesh_1.GetMesh(), False, False )
    
    # refine triangles
    tria_pattern = getTriaPattern(Mesh_1)
    tria_pattern.ApplyToMeshFaces( Mesh_1.GetMesh(), faces, 1, False)
    tria_pattern.MakeMesh( Mesh_1.GetMesh(), False, False )
    
    #Delete coincident nodes
    coincident_nodes = mesh_editor_0.FindCoincidentNodes( tol )
    mesh_editor_0.MergeNodes(coincident_nodes)
    print "\nInformation about the Boat mesh after pattern applying:"
    print "Number of nodes      : ", Mesh_1.GetMesh().NbNodes()
    print "Number of edges      : ", Mesh_1.GetMesh().NbEdges()
    print "Number of quadrangles: ", Mesh_1.GetMesh().NbQuadrangles()

if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)
