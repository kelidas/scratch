import geompy
import salome
import smesh
import math
gg = salome.ImportComponentGUI( "GEOM" )


length = 1000
height = 200
x1 = -length / 2.
y1 = 0
x2 = length / 2.
y2 = 0

x3 = length / 2.
y3 = height
x4 = -length / 2.
y4 = height

# create vertices
p1 = geompy.MakeVertex( x1, y1, 0. )
p2 = geompy.MakeVertex( x2, y2, 0. )
p3 = geompy.MakeVertex( x3, y3, 0. )
p4 = geompy.MakeVertex( x4, y4, 0. )

geompy.addToStudy( p1, "pnt1" )
geompy.addToStudy( p2, "pnt2" )
geompy.addToStudy( p3, "pnt3" )
geompy.addToStudy( p4, "pnt4" )

# create a vector on two points
v12 = geompy.MakeVector( p1, p2 )

# create a plane from a point, a vector and a trimsize
plane1 = geompy.MakePlaneThreePnt( p1, p2, p3, 0 )

# add objects in the study
id_plane1 = geompy.addToStudy( plane1, "Plane1" )


line1 = geompy.MakeEdge( p1, p2 )
line2 = geompy.MakeEdge( p2, p3 )
line3 = geompy.MakeEdge( p3, p4 )
line4 = geompy.MakeEdge( p4, p1 )
geompy.addToStudy( line1, "line1" )
geompy.addToStudy( line2, "line2" )
geompy.addToStudy( line3, "line3" )
geompy.addToStudy( line4, "line4" )

face1 = geompy.MakeFaceWires( [line1, line2, line3, line4], 1 )
geompy.addToStudy( face1, "face1" )


Mesh = smesh.Mesh( face1, 'Mesh_face' )

algo1D = Mesh.Segment()
algo1D.MaxSize( 10 )
algo2D = Mesh.Quadrangle()

Mesh.Compute()



if not Mesh.Compute():
    print 'Mesh computation failed!!!'
else:
    # Print information about the mesh
    print "Information about mesh:"
    print "Number of nodes       : ", Mesh.NbNodes()
    print "Number of edges       : ", Mesh.NbEdges()
    print "Number of faces       : ", Mesh.NbFaces()
    print "          triangles   : ", Mesh.NbTriangles()
    print "          quadrangles : ", Mesh.NbQuadrangles()
    print "          polygons    : ", Mesh.NbPolygons()
    print "Number of volumes     : ", Mesh.NbVolumes()
    print "          tetrahedrons: ", Mesh.NbTetras()
    print "          hexahedrons : ", Mesh.NbHexas()
    print "          prisms      : ", Mesh.NbPrisms()
    print "          pyramids    : ", Mesh.NbPyramids()
    print "          polyhedrons : ", Mesh.NbPolyhedrons()



#gg.createAndDisplayGO(id_plane1)
#gg.setDisplayMode(id_plane1,1)
#gg.setTransparency(id_plane1,0.5)

# create a rectangle in OXY plane
#face1 = geompy.MakeFaceHW(length, height, 1)

# add objects in the study
#id_face1  = geompy.addToStudy(face1,"Face1")

# display rectangles
#gg.createAndDisplayGO(id_face1)


print 'Done!'
