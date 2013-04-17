import salome
import geompy
import smesh, SMESH
import math

# Create Arete Variable = 100
Arete = 100

# Create 8 points corresponding to the box vertices and its centre (Origine = (0,0,0), Diag=(Arete,Arete,Arete,))

pnt1 = geompy.MakeVertex ( 0, 0, 0 )
pnt2 = geompy.MakeVertex ( Arete, 0, 0 )
pnt3 = geompy.MakeVertex ( Arete, Arete, 0 )
pnt4 = geompy.MakeVertex ( 0, Arete, 0 )
pnt5 = geompy.MakeVertex ( Arete, Arete, Arete )
pnt6 = geompy.MakeVertex ( 0, Arete, Arete )
pnt7 = geompy.MakeVertex ( 0, 0, Arete )
pnt8 = geompy.MakeVertex ( Arete, 0, Arete )
pnt_center = geompy.MakeVertex ( Arete / 2, Arete / 2, Arete / 2 )

geompy.addToStudy( pnt1, "pnt1" )
geompy.addToStudy( pnt2, "pnt2" )
geompy.addToStudy( pnt3, "pnt3" )
geompy.addToStudy( pnt4, "pnt4" )
geompy.addToStudy( pnt5, "pnt5" )
geompy.addToStudy( pnt6, "pnt6" )
geompy.addToStudy( pnt7, "pnt7" )
geompy.addToStudy( pnt8, "pnt8" )
geompy.addToStudy( pnt_center, "pnt_center" )

# Create 4 edges which form a face

line1 = geompy.MakeEdge( pnt1, pnt2 )
line2 = geompy.MakeEdge( pnt2, pnt3 )
line3 = geompy.MakeEdge( pnt3, pnt4 )
line4 = geompy.MakeEdge( pnt4, pnt1 )
geompy.addToStudy( line1, "line1" )
geompy.addToStudy( line2, "line2" )
geompy.addToStudy( line3, "line3" )
geompy.addToStudy( line4, "line4" )

face1 = geompy.MakeFaceWires( [line1, line2, line3, line4], 1 )
geompy.addToStudy( face1, "face1" )

# Create the 1st box by 2 points

box1 = geompy.MakeBoxTwoPnt( pnt1, pnt5 )
geompy.addToStudy( box1, "box1" )

# Create the 2nd box by extrusion of the reference face.

box2 = geompy.MakePrism( face1, pnt1, pnt7 )
geompy.addToStudy( box2, "box2" )

# Create 2 other faces of the box with 2 rotations of the reference face.

angle = 90 * math.pi / 180
face2 = geompy.MakeRotation( face1, line1, angle )
face3 = geompy.MakeRotation( face1, line4, angle )
geompy.addToStudy( face2, "face2" )
geompy.addToStudy( face3, "face3" )

# Use central symmetry on 3 created faces to build 6 faces of the 3rd box

face4 = geompy.MakeMirrorByPoint( face1, pnt_center )
face5 = geompy.MakeMirrorByPoint( face2, pnt_center )
face6 = geompy.MakeMirrorByPoint( face3, pnt_center )
geompy.addToStudy( face4, "face4" )
geompy.addToStudy( face5, "face5" )
geompy.addToStudy( face6, "face6" )

# Create the shell from 6 faces

Shell = geompy.MakeShell( [face1, face2, face3,
                          face4, face5, face6] )
geompy.addToStudy( Shell, "Shell" )

# Create the 3rd box from shell

box3 = geompy.MakeSolid( [Shell] )
geompy.addToStudy( box3, "box3" )

# Explode the 1rd box to reconstruct Edges.

edgeList = geompy.SubShapeAll( box1, geompy.ShapeType["EDGE"] )
i = 0
for edge in edgeList :
    name = geompy.SubShapeName( edge, box1 )
    id_SubEdge = geompy.addToStudyInFather( box1, edge, name )

# Create group of edges to build SubMesh.

edge1 = salome.myStudy.FindObjectByPath( "/Geometry/box1/Edge_6" ).GetObject()
edge2 = salome.myStudy.FindObjectByPath( "/Geometry/box1/Edge_7" ).GetObject()
edge3 = salome.myStudy.FindObjectByPath( "/Geometry/box1/Edge_12" ).GetObject()
group1 = geompy.CreateGroup( box1, geompy.ShapeType["EDGE"] )
geompy.UnionList( group1, [edge1, edge2, edge3] )

####################x
# Mesh
#####################



# Definition of the geometry for meshing in 3D:

Mesh_1 = smesh.Mesh( box1 )

# Definition of hypotheses and algorithms 1D, 2D and 3D :

Regular_1D = Mesh_1.Segment()
Nb_Segments_1 = Regular_1D.NumberOfSegments( 10 )
Nb_Segments_1.SetDistrType( 0 )
Quadrangle_2D = Mesh_1.Quadrangle()
Hexa_3D = Mesh_1.Hexahedron()

# Launch of the mesh computation:

isDone = Mesh_1.Compute()
if not isDone : print "Mesh is not computed"

# Create Submesh on Group of Edges (group1)

Nb_Segments_2 = smesh.smesh.CreateHypothesis( 'NumberOfSegments', 'StdMeshersEngine' )
Nb_Segments_2.SetNumberOfSegments( 10 )
Nb_Segments_2.SetScaleFactor( 0.5 )
SubMesh_1 = Mesh_1.GetSubMesh( group1, 'SubMesh_1' )
status = Mesh_1.AddHypothesis( Regular_1D, group1 )
status = Mesh_1.AddHypothesis( Nb_Segments_2, group1 )
isDone = Mesh_1.Compute()
if not isDone : print "Mesh is not computed"



