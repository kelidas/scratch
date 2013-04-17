#Copyright Open CASCADE 2007
#Author Edward Agapov
#Example of improved quadrangle mapping algorithm

import geompy, smesh
import os, sys

dir="/home/kelidas/Desktop/salome_examples/"
fileName = os.path.join( dir, "boat.brep" )

file_exist = os.path.exists(fileName)
if not file_exist :
    raise RuntimeError, "Please put the 'boat.brep' file into the directory that salome was started, or change the path in the python script manually"

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

if not Mesh_1.Compute():
    print 'Mesh computation failed!!!'
else:
    print "Information about the Boat mesh:"
    print "Number of nodes      : ", Mesh_1.GetMesh().NbNodes()
    print "Number of edges      : ", Mesh_1.GetMesh().NbEdges()
    print "Number of triangles  : ", Mesh_1.GetMesh().NbTriangles()
    print "Number of quadrangles: ", Mesh_1.GetMesh().NbQuadrangles()

if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)
