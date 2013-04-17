# Nom du chichier : Eprouvette de traction_1_trial.py
# Date de création : 20100508
# Auteur : Gwen MESSE

# RESUME : Ce fichier a pour but de :
# 1 Finalisser la géométrie d'une éprouvette de traction standard directement via python et salome
# 2 Finaliser le maillage quadrangulaire du modèle avec un bon ratio (exécution en python du maillage extrudé)
# 3 Finaliser les prérequis d'un fichier de commande python de dessin afin d'obtenir un template robuste.
# 4 Finaliser la création de groupe de maille directement à partir du maillage (découplage salome/code aster)


import geompy
import salome
# only for mesh
import smesh
gg = salome.ImportComponentGUI("GEOM")

#+++++++++++++++++++++++++++++++++++++++
# Description de la geometrie
#+++++++++++++++++++++++++++++++++++++++
#
# Point de référence du repère orthonormé
P000 = geompy.MakeVertex(0., 0., 0.)
#
# Vecteurs de référence du repère orthonormé
Vx = geompy.MakeVectorDXDYDZ(1., 0., 0.)
Vy = geompy.MakeVectorDXDYDZ(0., 1., 0.)
Vz = geompy.MakeVectorDXDYDZ(0., 0., 1.)
#
# Plans de référence du repère orthonormé
PXOY = geompy.MakePlane(P000, Vx, 100.)
PYOZ = geompy.MakePlane(P000, Vy, 100.)
PZOX = geompy.MakePlane(P000, Vz, 100.)
#
# Ajout des objets dans l'étude
id_P000 = geompy.addToStudy(P000, "Vertex P000")
id_Vx = geompy.addToStudy(Vx, "Vector Vx")
id_Vy = geompy.addToStudy(Vy, "Vector Vy")
id_Vz = geompy.addToStudy(Vz, "Vector Vz")
id_PXOY = geompy.addToStudy(P000, "Plane PXOY")
id_PYOZ = geompy.addToStudy(P000, "Plane PYOZ")
id_PZOX = geompy.addToStudy(P000, "Plane PZOX")
#
# Affichage des objets
gg.createAndDisplayGO(id_P000)
gg.createAndDisplayGO(id_Vx)
gg.createAndDisplayGO(id_Vy)
gg.createAndDisplayGO(id_Vz)
gg.createAndDisplayGO(id_PXOY)
gg.createAndDisplayGO(id_PYOZ)
gg.createAndDisplayGO(id_PZOX)
#
#+++++++++++++++++++++++++++++++++++++++
#
# Notes:
# 1 Les dimensions sont en mm
# 2 Les efforts sont en N
# 3 Les contraintes sont donc exprimées en N/mm2 soit en MPa
#
#=======================================
# Points
#=======================================
# Liste des points
#
# Points de la géométrie
P001 = geompy.MakeVertex(0., 5., 2.8)
P002 = geompy.MakeVertex(27., 5., 2.8)
P003 = geompy.MakeVertex(27., 18., 2.8)
P004 = geompy.MakeVertex(40., 18., 2.8)
P005 = geompy.MakeVertex(74.5, 18., 2.8)
P006 = geompy.MakeVertex(74.5, 0., 2.8)
P007 = geompy.MakeVertex(0., 0., 2.8)
#
# Ajout des objets dans l'étude
id_P001 = geompy.addToStudy(P001, "Vertex P001")
id_P002 = geompy.addToStudy(P002, "Vertex P002")
id_P003 = geompy.addToStudy(P003, "Vertex P003")
id_P004 = geompy.addToStudy(P004, "Vertex P004")
id_P005 = geompy.addToStudy(P005, "Vertex P005")
id_P006 = geompy.addToStudy(P006, "Vertex P006")
id_P007 = geompy.addToStudy(P007, "Vertex P007")
#
# Affichage des objets
gg.createAndDisplayGO(id_P001)
gg.createAndDisplayGO(id_P002)
gg.createAndDisplayGO(id_P003)
gg.createAndDisplayGO(id_P004)
gg.createAndDisplayGO(id_P005)
gg.createAndDisplayGO(id_P006)
gg.createAndDisplayGO(id_P007)
#
#=======================================
# LIGNES
#=======================================
# Liste des lignes
#
# Création des différents éléments linéaires
L001 = geompy.MakeLineTwoPnt(P001, P002)
L002 = geompy.MakeArcCenter(P003, P004, P002, 0)
L003 = geompy.MakeLineTwoPnt(P004, P005)
L004 = geompy.MakeLineTwoPnt(P005, P006)
L005 = geompy.MakeLineTwoPnt(P006, P007)
L006 = geompy.MakeLineTwoPnt(P007, P001)
#
# Ajout des objets dans l'étude
id_L001 = geompy.addToStudy(L001, "Line L001")
id_L002 = geompy.addToStudy(L002, "Line L002")
id_L003 = geompy.addToStudy(L003, "Line L003")
id_L004 = geompy.addToStudy(L004, "Line L004")
id_L005 = geompy.addToStudy(L005, "Line L005")
id_L006 = geompy.addToStudy(L006, "Line L006")
#
# Affichage des objets
gg.createAndDisplayGO(id_L001)
gg.createAndDisplayGO(id_L002)
gg.createAndDisplayGO(id_L003)
gg.createAndDisplayGO(id_L004)
gg.createAndDisplayGO(id_L005)
gg.createAndDisplayGO(id_L006)
#
#=======================================
# WIRES
#=======================================
# Liste des enveloppes filaires
#
# Création du 1/4 de modèle filaire externe fermé
W001 = geompy.MakeWire([L001, L002, L003, L004, L005, L006])
#
# Ajout des objets dans l'étude
id_W001 = geompy.addToStudy(W001, "Wire W001")
#
# Affichage des objets
gg.createAndDisplayGO(id_W001)
#
#=======================================
# FACES
#=======================================
# Liste des faces
#
# Création de la face du modèle
#F001 = geompy.MakeFaceWires([W001], 1)
F001 = geompy.MakeFace(W001, 1)
# Note the both two solutions work fine, think about the fact that when you have a check box for sentence 1 = yes and 0 = no
#
# Ajout des objets dans l'étude
id_F001 = geompy.addToStudy(F001, "Face F001")
#
# Affichage des objets
gg.createAndDisplayGO(id_F001)
#
#=======================================
# VOLUMES
#=======================================
# Liste des Volume
#
# Création du volume par extrusion
# Création du vecteur d'extrusion par ses composants
vector1 = geompy.MakeVectorDXDYDZ(0., 0., 1.)
# Création du 1/4 de volume extrudé
Vol14 = geompy.MakePrismVecH(F001, vector1, -5.6)
#
# Ajout des objets dans l'étude
id_vector1 = geompy.addToStudy(vector1,"Vector1")
id_Vol14 = geompy.addToStudy(Vol14, "Vol14")
#
# Affichage des objets
gg.createAndDisplayGO(id_vector1)
gg.createAndDisplayGO(id_Vol14) 

print "message : geom computed"

#+++++++++++++++++++++++++++++++++++++++
# Description du maillage
#+++++++++++++++++++++++++++++++++++++++
import GHS3DPlugin
import StdMeshers
import NETGENPlugin
#
#
#
# Création du maillage
Mesh_1 = smesh.Mesh(F001, "Mesh_1")
#
# Algorithme 1D
Regular_1D = Mesh_1.Segment()
Average_length_1 = Regular_1D.LocalLength(0.7)
Average_length_1.SetPrecision( 1e-07 )
#
# Algorithme 2D
Netgen_2D = Mesh_1.Triangle(algo=smesh.NETGEN_2D)
Max_Element_Area_1 = Netgen_2D.MaxElementArea(0.49)
Quadrangle_Preference_1 = Netgen_2D.SetQuadAllowed()
isDone = Mesh_1.Compute()
#
# Algorithme 3D (Extrusion le long d'un vecteur)
Mesh_1.ExtrusionSweepObject2D(Mesh_1, smesh.DirStruct(smesh.PointStruct(0., 0., -0.7)), 8)
#
print "message : mesh computed"

# Création des groupes de mailles
# Afin d'éviter une mauvaise prise en compte du passage entre salome 
# et code aster le groupe de maille se fait à partir du maillage
#
aFilterManager = smesh.CreateFilterManager()
#
# Création du filtre
aFilter_1 = aFilterManager.CreateFilter()
aCriteria = []
# test commande de critère
#
# page de référence
# http://docs.salome-platform.org/salome_5_1_3/smesh/dev/structSMESH_1_1Filter_1_1Criterion.html
# http://docs.salome-platform.org/salome_5_1_3/smesh/dev/namespaceSMESH.html
#
# RELATED DOCS
#
# http://docs.salome-platform.org/salome_5_1_3/smesh/dev/structSMESH_1_1Filter_1_1Criterion.html
# http://docs.salome-platform.org/salome_5_1_3/smesh/dev/namespaceSMESH.html
# http://docs.salome-platform.org/salome_5_1_3/smesh/dev/functions_0x70.html#index_p
# http://www.salome-platform.org/user-section/tui-examples
# http://bugs.gentoo.org/attachment.cgi?id=114660&action=view
# 
##
#aCriterion = smesh.Filter.Criterion(long_Type, long_Compare, double_Threshold, string_ThresholdStr, string_ThresholdID, long_UnaryOp, ...
#...long_BinaryOp, double_Tolerance, ElementType_TypeOfElement, long_Precision)
#
aCriterion = smesh.Filter.Criterion(smesh.BelongToGeom,smesh.EqualTo,0,'Plane PYOZ','',32,32,1e-07,smesh.Face,-1)
##
#aCriterion = smesh.Filter.Criterion(17,32,0,'PYOZ','',32,32,1e-07,smesh.Face,-1)
##
#aCriterion = SMESH.Filter.Criterion(14,27,0,'Edge_3',salome.ObjectToID(Edge_3),27,25,1e-07,SMESH.EDGE,-1)
##
aBelongToPlane_1 = aFilterManager.CreateBelongToPlane()
aBelongToPlane_1.SetTolerance(1e-07)
aCriteria.append(aCriterion)
aFilter_1.SetCriteria(aCriteria)
aFilter_1.SetPredicate(aBelongToPlane_1)
cd = Mesh_1.CreateEmptyGroup(ssmesh.Face, 'cd' )






