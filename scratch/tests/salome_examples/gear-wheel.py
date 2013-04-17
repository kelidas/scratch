import math
import salome
import geompy
import smesh

#########################################
#
# Gear Wheel Parameters
#
#########################################

h_thick = 20.
h_thin  = 7.

mesh_nb_segments = 10
mesh_nb_segments_local = int(mesh_nb_segments * h_thin / h_thick)

nb_cogs = 6
nb_blocks = 2 * nb_cogs

#########################################
#
# Gear Wheel Geometry
#
#########################################

OO = geompy.MakeVertex(0, 0, 0)
Oz = geompy.MakeVectorDXDYDZ(0, 0, 200)

geompy.addToStudy(OO, "OO")
geompy.addToStudy(Oz, "Oz")

alpha = 360.0/nb_blocks/2.0
betta = alpha*2.0/3.0

radiuces = [21., 39., 57., 75., 100.]
angles   = [alpha, alpha, alpha, alpha, betta]
points   = [[], [], [], [], []]
arcs     = []
blocks   = []
multis_thick = []
multis_thin  = []

pp_local_hyp_1 = None

nb_arcs = len(radiuces)
for ii in range(nb_arcs):
	rr = radiuces[ii]
	aa = angles[ii]*math.pi/180.0

	pp_c = geompy.MakeVertex(rr, 0, 0)
	pp_n = geompy.MakeRotation(pp_c, Oz, -aa)
	pp_p = geompy.MakeRotation(pp_c, Oz,  aa)

	if ii == 0:
		pp_local_hyp_1 = pp_p
		pass

	geompy.addToStudy(pp_c, "point central rr=" + `rr`)
	geompy.addToStudy(pp_n, "point negative rr=" + `rr`)
	geompy.addToStudy(pp_p, "point positive rr=" + `rr`)

	arc = geompy.MakeArc(pp_n, pp_c, pp_p)
	geompy.addToStudy(arc, "arc rr=" + `rr`)

	points[ii] = [pp_n, pp_c, pp_p]
	arcs.append(arc)

	if ii > 0:
		face = geompy.MakeQuad2Edges(arcs[ii-1], arcs[ii])
		geompy.addToStudy(face, "bottom face " + `ii`)

		block_thick = geompy.MakePrismVecH(face, Oz, h_thick)
		geompy.addToStudy(block_thick, "block thick " + `ii`)

		blocks.append(block_thick)

		if ii < nb_arcs - 1:
			block_thin  = geompy.MakePrismVecH(face, Oz, h_thin)
			geompy.addToStudy(block_thin, "block thin " + `ii`)

			coords1 = geompy.PointCoordinates(points[ii-1][0])
			coords2 = geompy.PointCoordinates(points[ii  ][0])
			p_side = geompy.MakeVertex((coords1[0] + coords2[0])/2.0,
						   (coords1[1] + coords2[1])/2.0, 5)

			f_side_thick = geompy.GetFaceNearPoint(block_thick, p_side)
			ind_thick = geompy.LocalOp.GetSubShapeIndex(block_thick, f_side_thick)

			multi_thick = geompy.MakeMultiTransformation1D(block_thick, ind_thick, -1, nb_blocks)
			multis_thick.append(multi_thick)

			f_side_thin = geompy.GetFaceNearPoint(block_thin, p_side)
			ind_thin = geompy.LocalOp.GetSubShapeIndex(block_thin, f_side_thin)

			multi_thin = geompy.MakeMultiTransformation1D(block_thin, ind_thin, -1, nb_blocks)
			multis_thin.append(multi_thin)
			pass
		pass
	pass

cog  = geompy.MakeTranslation(blocks[nb_arcs - 2], 0, 0, h_thin)
cogs = geompy.MultiRotate1D(cog, Oz, nb_cogs)

compound_1 = geompy.MakeCompound(multis_thin)
compound_2 = geompy.MakeTranslation(compound_1, 0, 0, h_thin + h_thick)
compound_3 = geompy.MakeCompound(multis_thick)
compound_4 = geompy.MakeTranslation(compound_3, 0, 0, h_thin)

compound_5 = geompy.MakeCompound([compound_1, compound_2, compound_4, cogs])

# Finally we have the Gear Wheel geometry
gear_wheel = geompy.MakeGlueFaces(compound_5, 1e-05)
geompy.addToStudy(gear_wheel, "Gear wheel")

# Find two edges to assign on them local hypotheses

pp_local_hyp_2 = geompy.MakeTranslation(pp_local_hyp_1, 0, 0, h_thin)

pp_local_hyp_3 = geompy.MakeTranslation(pp_local_hyp_2, 0, 0, h_thick)
pp_local_hyp_4 = geompy.MakeTranslation(pp_local_hyp_3, 0, 0, h_thin)

ee_local_hyp_1 = geompy.GetEdge(gear_wheel, pp_local_hyp_1, pp_local_hyp_2)
ee_local_hyp_2 = geompy.GetEdge(gear_wheel, pp_local_hyp_3, pp_local_hyp_4)

geompy.addToStudyInFather(gear_wheel, ee_local_hyp_1, "ee_local_hyp_1")
geompy.addToStudyInFather(gear_wheel, ee_local_hyp_2, "ee_local_hyp_2")

#########################################
#
# Gear Wheel Mesh
#
#########################################

gear_mesh = smesh.Mesh(gear_wheel)

# Assign hypotheses and algorithms
algo1D = gear_mesh.Segment()
algo1D.NumberOfSegments(mesh_nb_segments)
gear_mesh.Quadrangle()
gear_mesh.Hexahedron()

algo1D_local_1 = gear_mesh.Segment(ee_local_hyp_1)
algo1D_local_1.NumberOfSegments(mesh_nb_segments_local)
algo1D_local_1.Propagation()

algo1D_local_2 = gear_mesh.Segment(ee_local_hyp_2)
algo1D_local_2.NumberOfSegments(mesh_nb_segments_local)
algo1D_local_2.Propagation()

# Compute the mesh
isDone = gear_mesh.Compute()
if not isDone: print 'Mesh computation failed'

# Update Object Browser
if salome.sg.hasDesktop():
	salome.sg.updateObjBrowser(1)
