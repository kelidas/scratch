# This file is a modification of the original one downloaded from the web page of Erwan ADAM
# Our intention is to automatize the mesh creation and saving for general more complex geometries
### ----------------------------------------------------------------------------------------
# Automatic procedure for the mesh described in CAELinux Tutorial 1 by Joel Cugnoni
### ----------------------------------------------------------------------------------------
# ----------
import string

in_tui = 1
print "Embedded python"

### in_tui = 0
### print "External python ('batch mode')"


# -------------
# Class SalomeSession to lanuch the services of salome
# in 'batch mode' then to close this services at the
# end of the script ... Of course, this class should be
# defined elsewhere but for the script to be self-consistent
# I've put it here
# -------------

class SalomeSession(object):
    
    def getKRD(self):
        import os
        KERNEL_ROOT_DIR = os.getenv("KERNEL_ROOT_DIR")
        if KERNEL_ROOT_DIR is None:
            msg  = '\n\n'
            msg += 'KERNEL_ROOT_DIR not defined ...\n'
            msg += 'Be sure you are in salome environement.\n'
            raise Exception(msg)
        return KERNEL_ROOT_DIR
    
    def __init__(self, modules):
        #
        # Save (copy) the real user arguments
        #
        import sys
        argv_ini = sys.argv[:]
        #
        # Do like a runSalome --modules=... --logger -- terminal
        #
        import sys
        sys.argv  = ['bin/salome/runSalome.py']
        sys.argv += ['--modules=%s'%(",".join(modules))]
        sys.argv += ['--logger']
        sys.argv += ['--terminal']
        sys.argv += ['--standalone=pyContainer']
        #
        # Find a free port for naming service
        #
        port = self.searchFreePort()
        # --
        # E.A. : sys.path.insert(0, KERNEL_ROOT_DIR+"/bin/salome")
        # because there is multiple runSalome.py in V2_2_4 distribution
        # This will be removed after ...
        #
        KERNEL_ROOT_DIR = self.getKRD()
        sys.path.insert(0, KERNEL_ROOT_DIR+"/bin/salome")
        #
        import runSalome
        self.runSalome = runSalome
        clt, args = runSalome.main()
        runSalome.clt, runSalome.args = clt, args
        self.port = runSalome.args['port']
        self.naming_service = clt
        self.orb = clt.orb
        from LifeCycleCORBA import LifeCycleCORBA
        lcc = LifeCycleCORBA(clt.orb)
        self.lcc = lcc
        #
        # revert to the user args
        #
        import sys
        sys.argv = argv_ini
        #
        return
    
    def searchFreePort(self):
        print "Searching a free port for naming service:",
        NSPORT=2810
        limit=NSPORT
        limit=limit+100
        while 1:
            print "%s "%(NSPORT),
            import os
            status = os.system("netstat -ltn | grep -E :%s"%(NSPORT))
            if status:
                home = os.environ['HOME']
                from os import getpid
                tmp_file = '/tmp/hostname_%s'%(getpid())
                from os import system
                system('hostname > %s'%(tmp_file))
                f = open(tmp_file)
                hostname = f.read()
                hostname = hostname[:-1]
                f.close()
                system('rm -f %s'%(tmp_file))
                os.environ['OMNIORB_CONFIG'] = '%s/.omniORB_%s.cfg'%(home, NSPORT)
                f = open(os.environ['OMNIORB_CONFIG'], "w")
                f.write("ORBInitRef NameService=corbaname::%s:%s\n"%(hostname, NSPORT))
                f.close()
                print "- Ok"
                break
            if NSPORT == limit:
                msg  = ""
                msg += "I Can't find a free port to launch omniNames\n"
                msg += "I suggest you to kill the running servers and try again.\n"
                raise msg
            NSPORT=NSPORT+1
            pass
        return NSPORT
    
    def __del__(self):
        try:
            port = self.port
        except:
            return
        from os import system
        system("killSalomeWithPort.py %s"%(port))
        return
    
    pass

#
# Import modules
#

if in_tui:
    import salome
    def updateStudy():
        salome.sg.updateObjBrowser(1)
        return
    from geompy import *
else:
    salome = SalomeSession(modules=['GEOM','SMESH'])
    def updateStudy():
        return
    from batchmode_geompy import *
    pass

#
# Construction of geometries
#

WantPlanarFace = 1

w1=MakeSketcher("Sketcher:F -0.5 -0.5:TT -0.5 0.5:TT 1.5 0.5:TT 1.5 -0.5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(w1,"w1")
updateStudy()
w1e=MakeSketcher("Sketcher:F -20 -20:TT -20 20:TT 20 20:TT 20 -20:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(w1e,"w1e")
updateStudy()
p1=MakeVertex(0.1,0.1,0.0)
addToStudy(p1,"p1")
updateStudy()
v1=MakeVectorDXDYDZ(0,0,1)
addToStudy(v1,"v1")
updateStudy()
f_prof=open('/home/kelidas/Desktop/salome_examples/profilo_T20.dat')
r_prof=f_prof.readlines()
f_prof.close()

pps=[]
for cc in r_prof:
    ccsp=cc.split()
    p1=MakeVertex(float(ccsp[0]), float(ccsp[1]), 0.0)
    pps.append(p1)

print pps

pol=MakeInterpol(pps)
addToStudy(pol,"pol")
updateStudy()

###c1=MakeCircle(p1,v1,0.025)
###addToStudy(c1,"c1")
###updateStudy()
w2=MakeWire([pol])
addToStudy(w2,"w2")
updateStudy()
f1=MakeFace(w1,WantPlanarFace)
addToStudy(f1,"f1")
updateStudy()
f2=MakeFace(w2,WantPlanarFace)
addToStudy(f2,"f2")
updateStudy()


f3c=MakeBoolean(f1,f2,2)
addToStudy(f3c,"f3c")
updateStudy()

wb_1=MakeSketcher("Sketcher:F -5 0.5:TT -5 5:TT -.5 5:TT -0.5 0.5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_1,"wb_1")
updateStudy()
fb_1=MakeFace(wb_1,WantPlanarFace)
addToStudy(fb_1,"fb_1")
updateStudy()
wb_2=MakeSketcher("Sketcher:F -0.5 0.5:TT -0.5 5:TT 1.5 5:TT 1.5 0.5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_2,"wb_2")
updateStudy()
fb_2=MakeFace(wb_2,WantPlanarFace)
addToStudy(fb_2,"fb_2")
updateStudy()
wb_3=MakeSketcher("Sketcher:F 1.5 0.5:TT 1.5 5:TT 6 5:TT 6 0.5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_3,"wb_3")
updateStudy()
fb_3=MakeFace(wb_3,WantPlanarFace)
addToStudy(fb_3,"fb_3")
updateStudy()

wb_4=MakeSketcher("Sketcher:F -5 -0.5:TT -5 0.5:TT -0.5 0.5:TT -0.5 -0.5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_4,"wb_4")
updateStudy()
fb_4=MakeFace(wb_4,WantPlanarFace)
addToStudy(fb_4,"fb_4")
updateStudy()
wb_5=MakeSketcher("Sketcher:F 1.5 -0.5:TT 1.5 0.5:TT 6 0.5:TT 6 -0.5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_5,"wb_5")
updateStudy()
fb_5=MakeFace(wb_5,WantPlanarFace)
addToStudy(fb_5,"fb_5")
updateStudy()

wb_6=MakeSketcher("Sketcher:F -5 -5:TT -5 -0.5:TT -0.5 -0.5:TT -0.5 -5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_6,"wb_6")
updateStudy()
fb_6=MakeFace(wb_6,WantPlanarFace)
addToStudy(fb_6,"fb_6")
updateStudy()
wb_7=MakeSketcher("Sketcher:F -0.5 -5:TT -0.5 -0.5:TT 1.5 -0.5:TT 1.5 -5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_7,"wb_7")
updateStudy()
fb_7=MakeFace(wb_7,WantPlanarFace)
addToStudy(fb_7,"fb_7")
updateStudy()
wb_8=MakeSketcher("Sketcher:F 1.5 -5:TT 1.5 -0.5:TT 6 -0.5:TT 6 -5:WW",[0,0,0, 0,0,1, 1,0,0])
addToStudy(wb_8,"wb_8")
updateStudy()
fb_8=MakeFace(wb_8,WantPlanarFace)
addToStudy(fb_8,"fb_8")
updateStudy()

ff1_b=MakeBoolean(fb_1,fb_2,3)
ff1=MakeBoolean(ff1_b,fb_3,3)
ff2_b=MakeBoolean(fb_4,f3c,3)
ff2=MakeBoolean(ff2_b,fb_5,3)
ff3_b=MakeBoolean(fb_6,fb_7,3)
ff3=MakeBoolean(ff3_b,fb_8,3)

fff1_b=MakeBoolean(ff1,ff2,3)
fff1=MakeBoolean(fff1_b,ff3,3)



#
# Construction of the mesh tetra
#

import StdMeshers
import SMESH
smesh = salome.lcc.FindOrLoadComponent("FactoryServer", "SMESH")
smesh.SetCurrentStudy(myStudy)

mesh2d = smesh.CreateMesh(fff1)
ior  = salome.orb.object_to_string(mesh2d)
sobj = myStudy.FindObjectIOR(ior)
attr = sobj.FindAttribute("AttributeName")[1]
attr.SetValue("AIR_TETRA")

hyp1d = smesh.CreateHypothesis("Regular_1D", "libStdMeshersEngine.so")
hyp2d = smesh.CreateHypothesis("MEFISTO_2D", "libStdMeshersEngine.so")

hyp1d_2 = smesh.CreateHypothesis("Regular_1D","libStdMesherEngine.so")
hyp1d_3 = smesh.CreateHypothesis("Regular_1D", "libStdMeshersEngine.so")

hyp2d_q = smesh.CreateHypothesis("Quadrangle_2D", "libStdMeshersEngine.so")

algo1d = smesh.CreateHypothesis("NumberOfSegments", "libStdMeshersEngine.so")
algo1d.SetNumberOfSegments(10)
algo2d = smesh.CreateHypothesis("MaxElementArea", "libStdMeshersEngine.so")
algo2d.SetMaxElementArea(.1)

algo1d_2 = smesh.CreateHypothesis("NumberOfSegments", "libStdMeshersEngine.so")
algo1d_2.SetNumberOfSegments(200)
algo1d_3 = smesh.CreateHypothesis("NumberOfSegments", "libStdMeshersEngine.so")
algo1d_3.SetNumberOfSegments(16)

my_edges=SubShapeAll(fff1,ShapeType["EDGE"])
print len(my_edges)
i=0
for edg in my_edges:
    i=i+1
    print i
    addToStudy(edg,"myedg_"+str(i))
    updateStudy()

my_faces=SubShapeAll(fff1,ShapeType["FACE"])
print len(my_faces)
i=0
for edg in my_faces:
    i=i+1
    print i
    addToStudy(edg,"myface_"+str(i))
    updateStudy()
    
for tool in [hyp1d, hyp2d_q, algo1d]:
    mesh2d.AddHypothesis(fff1, tool)
    pass

#mesh2d.AddHypothesis(my_edges[0],hyp1d_3)
#mesh2d.AddHypothesis(my_edges[0],algo1d_3)
#mesh2d.AddHypothesis(my_edges[3],hyp1d_3)
#mesh2d.AddHypothesis(my_edges[3],algo1d_3)
mesh2d.AddHypothesis(my_faces[4],hyp1d)
mesh2d.AddHypothesis(my_faces[4],algo1d)
mesh2d.AddHypothesis(my_faces[4],hyp2d)
mesh2d.AddHypothesis(my_faces[4],algo2d)

mesh2d.AddHypothesis(my_edges[15],hyp1d_2)
mesh2d.AddHypothesis(my_edges[15],algo1d_2)


b = smesh.Compute(mesh2d, fff1)
if in_tui:
    smeshgui = salome.ImportComponentGUI("SMESH")
    smeshgui.Init(salome.myStudyId)
    smeshgui.SetMeshIcon(salome.ObjectToID(mesh2d), b )
    pass

updateStudy()

file_name = "air_tetra.med"
from os import system
system("rm -f %s > /dev/null 2>&1"%(file_name))
file_name="/home/edmondo/Documents/DOWN/air_tetra.med"
mesh2d.ExportMED(file_name, 0)



