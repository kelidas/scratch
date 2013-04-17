#Copyright Open CASCADE 2007
#Author  :  ZHIVOTOVSKY Grigory

# Build and mesh a hull of a dry cargo ship Kishinev
# Basic ship data
# Length overall 123.5 m
# Scantling length 117 m
# Breadth moulded 15 m
# Depth at strength deck 6.5 m
# Scantling draft 4.5 m

import geompy, smesh

#Build geometry
#Define bow 
#Build vertices
Vertex_Bow1 = geompy.MakeVertex(120,0.,4.5)
Vertex_Bow2 = geompy.MakeVertex(120.632,0., 5.253)
Vertex_Bow3 = geompy.MakeVertex(121.263,0.,6.643)
#Build  bow curve 
Bow = geompy.MakeInterpol([Vertex_Bow1, Vertex_Bow2, Vertex_Bow3])
#Define aft 
#Build vertices
Vertex_Aft1 = geompy.MakeVertex(0.,0.,4.5)
Vertex_Aft2 = geompy.MakeVertex(-1.263,0.,5.1)
Vertex_Aft3 = geompy.MakeVertex(-2.5,0.,6.2)
Vertex_Aft4 = geompy.MakeVertex(-2.526,0.,6.643)
#Build aft curve 
Aft = geompy.MakeInterpol([Vertex_Aft1, Vertex_Aft2, Vertex_Aft3, Vertex_Aft4])
#Define frames
Curve=[Bow]
#Define coordinates of vertices for each frame
#coordinates of vertices for frame 10 
XYZ_Frame_1 = [[120,0.,4.5], [120,1.216, 6.643]]
#coordinates of vertices for frame 9 1/2
XYZ_Frame_2 = [[114, 0., 0.12], [114, 1.622, 2.357], [114, 3.041, 4.5], [114, 4.257, 6.643]]
#coordinates of vertices for frame 9
XYZ_Frame_3 = [[108, 0., 0.], [108, 3.041, 2.357], [108, 5.068, 4.5], [108, 6.284, 6.643]]
#coordinates of vertices for frame 8 1/2
XYZ_Frame_4 = [[102, 0., 0.],[102, 0.608, 0.], [102, 4.865, 2.357], [102, 6.486, 4.5], [102, 7.297, 6.643]]
#coordinates of vertices for frame 8
XYZ_Frame_5 = [[96, 0., 0.], [96, 0.9, 0.], [96, 1.8, 0.], [96, 2.7, 0.], [96, 3.2, 0.], [96, 3.649, 0.], [96, 6.284, 2.357], [96, 7.095, 4.5], [96, 7.5, 6.643]]
#coordinates of vertices for frame 7
XYZ_Frame_6 = [[84, 0., 0.], [84, 1.9, 0.], [84, 3.8, 0.], [84, 5.2, 0.], [84, 5.676, 0.], [84, 6.689, 0.429], [84, 7.297, 1.071], [84, 7.5, 2.357],[84, 7.5, 4.5], [84, 7.5, 6.643]]
#coordinates of vertices for frame 6
XYZ_Frame_7 = [[72, 0., 0.], [72, 1.9, 0.], [72, 3.8, 0.], [72, 5.2, 0.], [72, 5.676, 0.], [72, 6.689, 0.429], [72, 7.297, 1.071], [72, 7.5, 2.357],[72, 7.5, 4.5], [72, 7.5, 6.643]]
#coordinates of vertices for frame 5
XYZ_Frame_8 = [[60, 0., 0.], [60, 1.9, 0.], [60, 3.8, 0.], [60, 5.2, 0.], [60, 5.676, 0.], [60, 6.689, 0.429], [60, 7.297, 1.071], [60, 7.5, 2.357],[60, 7.5, 4.5], [60, 7.5, 6.643]]
#coordinates of vertices for frame 4
XYZ_Frame_9 = [[48, 0., 0.], [48, 1.9, 0.], [48, 3.8, 0.], [48, 5.2, 0.], [48, 5.676, 0.], [48, 6.689, 0.429], [48, 7.297, 1.071], [48, 7.5, 2.357],[48, 7.5, 4.5], [48, 7.5, 6.643]]
#coordinates of vertices for frame 3
XYZ_Frame_10 = [[36, 0., 0.], [36, 1.9, 0.], [36, 3.8, 0.], [36, 5.2, 0.], [36, 5.676, 0.], [36, 6.689, 0.429], [36, 7.297, 1.071], [36, 7.5, 2.357],[36, 7.5, 4.5], [36, 7.5, 6.643]]
#coordinates of vertices for frame 2
XYZ_Frame_11 = [[24, 0., 0.], [24, 1.9, 0.], [24, 3.8, 0.], [24, 5.2, 0.], [24, 5.676, 0.], [24, 6.689, 0.429], [24, 7.297, 1.071], [24, 7.5, 2.357],[24, 7.5, 4.5], [24, 7.5, 6.643]]
#coordinates of vertices for frame 1 1/2
XYZ_Frame_12 = [[18, 0., 0.], [18, 1.4, 0.], [18, 2.8, 0.], [18, 4.2, 0.], [18, 4.865, 0.], [18, 5.676, 0.429], [18, 6.689, 1.071], [18, 7.297, 2.357],[18, 7.5, 4.5], [18, 7.5, 6.643]]
#coordinates of vertices for frame 1
XYZ_Frame_13 = [[12, 0., 0.], [12, 0.7, 0.], [12, 1.5, 0.], [12, 2.2, 0.], [12, 2.432, 0.], [12, 3.649, 0.429], [12, 4.662, 1.071], [12, 5.676, 2.357],[12, 6.689, 4.5], [12, 7.297, 6.643]]
#coordinates of vertices for frame 1/2
XYZ_Frame_14 = [[6, 0.,2.357], [6, 3.041, 3.214], [6, 4.662, 4.5], [6, 5.98, 6.643]]
#coordinates of coordinates of vertices for frame 0
XYZ_Frame_15 = [[0.,0.,4.5], [0.,2.027,5.357], [0,2.838, 6.643]]
XYZ_Frame_point=[XYZ_Frame_1, XYZ_Frame_2,XYZ_Frame_3, XYZ_Frame_4, XYZ_Frame_5, XYZ_Frame_6, XYZ_Frame_7, XYZ_Frame_8, XYZ_Frame_9, XYZ_Frame_10, XYZ_Frame_11, XYZ_Frame_12, XYZ_Frame_13, XYZ_Frame_14, XYZ_Frame_15]
Vertex=[]
num_vertex=0
for i in range(len(XYZ_Frame_point)):    
    list_curve=[]
    j_max= len(XYZ_Frame_point[i])
    for j in range(j_max):
#Build j-th vertex for i-th frame
       Vertex_j = geompy.MakeVertex(XYZ_Frame_point [i][j][0], XYZ_Frame_point [i][j][1], XYZ_Frame_point [i][j][2])
       Vertex.append(Vertex_j)  
       list_curve.append(Vertex[j+num_vertex])
#Build i-th frame curve
    curve_i =  geompy.MakeInterpol(list_curve)  
    Curve.append(curve_i)
    num_vertex=num_vertex+j_max
    geompy.addToStudy( Curve[i], "Curve")    
Curve.append(Aft)
#Build shell for a half of the ship hull
shell = geompy.MakeThruSections(Curve, theModeSolid=0, thePreci = 0.0001, theRuled=1)
Vector_1 = geompy.MakeVectorDXDYDZ(0, 1, 0)
Plane_1 = geompy.MakePlane(Vertex_Aft2, Vector_1, 300)
#Build  symmetry shell to model the full ship hull using mirror through plane Oxz
Mirror_1 = geompy.MakeMirrorByPlane(shell, Plane_1)
Full_shell = geompy.MakeCompound([shell, Mirror_1])
geompy.addToStudy( shell, " shell")  
geompy.addToStudy(Full_shell, "Full_shell")
if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)

#Mesh creation:
#Wire discretisation; Nb.Segments=14
#Quadrangle(Mapping): QuadranglePreference

Mesh_1 = smesh.Mesh(shell, "Kishinev")
Wire_discretisation = Mesh_1.Segment()
Nb_Segments = Wire_discretisation.NumberOfSegments(14)
Nb_Segments.SetDistrType( 0 )
Quadrangle_Mapping = Mesh_1.Quadrangle()
Quadrangle_Preference = Quadrangle_Mapping.QuadranglePreference()

# Compute mesh for a half of the ship shell
if not Mesh_1.Compute():
    print 'Mesh computation failed!!!'
else:
    #Build mesh for the whole hull using Mirror through plane Oxz
    mesh_editor_0 = Mesh_1.GetMesh().GetMeshEditor()
    mesh_elements=Mesh_1.GetMesh().GetElementsId()
    mesh_editor_0.Mirror( mesh_elements, smesh.SMESH.AxisStruct( 0, 0, 0, 0, 1, 0 ), smesh.SMESH.SMESH_MeshEditor.PLANE, 1 )
    #Delete coincident nodes
    coincident_nodes = mesh_editor_0.FindCoincidentNodes( 1e-05 )
    mesh_editor_0.MergeNodes(coincident_nodes)
    
    print "Information about the Kishinev mesh:"
    print "Number of nodes      : ", Mesh_1.GetMesh().NbNodes()
    print "Number of edges      : ", Mesh_1.GetMesh().NbEdges()
    print "Number of triangles  : ", Mesh_1.GetMesh().NbTriangles()
    print "Number of quadrangles: ", Mesh_1.GetMesh().NbQuadrangles()
    
if geompy.salome.sg.hasDesktop():
    geompy.salome.sg.updateObjBrowser(1)
