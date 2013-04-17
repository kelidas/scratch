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

###w1=MakeSketcher("Sketcher:F -20 -20:TT -20 20:TT 20 20:TT 20 -20:WW",[0,0,0, 0,0,1, 1,0,0])
###addToStudy(w1,"w1")
###updateStudy()

p1=MakeVertex(0.5,0.0,0.0)
addToStudy(p1,"p1")
updateStudy()
p2=MakeVertex(-4.5,0.0,0.0)
addToStudy(p2,"p2")
updateStudy()
p3=MakeVertex(0.5,5.0,0.0)
addToStudy(p3,"p3")
updateStudy()
p4=MakeVertex(5.5,0.0,0.0)
addToStudy(p4,"p4")
updateStudy()
p5=MakeVertex(0.5,-5.0,0.0)
addToStudy(p5,"p5")
updateStudy()


p2_p=MakeVertex(-0.5,0.0,0.0)
addToStudy(p2_p,"p2_p")
updateStudy()
p3_p=MakeVertex(0.5,1.0,0.0)
addToStudy(p3_p,"p3_p")
updateStudy()
p4_p=MakeVertex(1.5,0.0,0.0)
addToStudy(p4_p,"p4_p")
updateStudy()
p5_p=MakeVertex(0.5,-1.0,0.0)
addToStudy(p5_p,"p5_p")
updateStudy()

a1g=MakeArc(p2,p3,p4)
a1p=MakeArc(p2_p,p3_p,p4_p)
l1=MakeLineTwoPnt(p2_p,p2)
l2=MakeLineTwoPnt(p4_p,p4)
a2g=MakeArc(p2,p5,p4)
a2p=MakeArc(p2_p,p5_p,p4_p)


w1ss=MakeWire([l1,a1g,l2,a1p])
addToStudy(w1ss,"w1ss")
updateStudy()
w1st=MakeWire([l1,a2g,l2,a2p])
addToStudy(w1st,"w1st")
updateStudy()
fw1ss=MakeFace(w1ss,WantPlanarFace)
addToStudy(fw1ss,"fw1ss")
updateStudy()
fw1st=MakeFace(w1st,WantPlanarFace)
addToStudy(fw1st,"fw1st")
updateStudy()

ffw1=MakeBoolean(fw1ss,fw1st,3)



v1=MakeVectorDXDYDZ(0,0,1)
addToStudy(v1,"v1")
updateStudy()
e1=MakeEllipse(p1,v1,2,1)
addToStudy(e1,"e1")
updateStudy()
c1=MakeCircle(p1,v1,5)
addToStudy(c1,"c1")
updateStudy()
f_prof=open('/home/kelidas/Desktop/salome_examples/profilo_T20.dat')
r_prof=f_prof.readlines()
f_prof.close()

pps=[]
for cc in r_prof:
    ccsp=cc.split()
    p1=MakeVertex(float(ccsp[0]), float(ccsp[1]), 0.0)
    pps.append(p1)



pol=MakeInterpol(pps)
addToStudy(pol,"pol")
updateStudy()
w1=MakeWire([c1])
addToStudy(w1,"w1")
updateStudy()
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

fff=MakeBoolean(f3c,ffw1,3)
addToStudy(fff,"fff")
updateStudy()


#
# Construction of the mesh tetra
#

import StdMeshers
import SMESH
smesh = salome.lcc.FindOrLoadComponent("FactoryServer", "SMESH")
smesh.SetCurrentStudy(myStudy)

mesh2d = smesh.CreateMesh(fff)
ior  = salome.orb.object_to_string(mesh2d)
sobj = myStudy.FindObjectIOR(ior)
attr = sobj.FindAttribute("AttributeName")[1]
attr.SetValue("TETRA_2D")

hyp1d = smesh.CreateHypothesis("Regular_1D", "libStdMeshersEngine.so")
hyp2d = smesh.CreateHypothesis("MEFISTO_2D", "libStdMeshersEngine.so")

hyp1d_2=smesh.CreateHypothesis("Regular_1D","libStdMesherEngine.so")

algo1d = smesh.CreateHypothesis("NumberOfSegments", "libStdMeshersEngine.so")
algo1d.SetNumberOfSegments(10)
###algo2d = smesh.CreateHypothesis("LengthFromEdges", "libStdMeshersEngine.so")
algo2d = smesh.CreateHypothesis("MaxElementArea", "libStdMeshersEngine.so")
algo2d.SetMaxElementArea(.2)
hyp2dq = smesh.CreateHypothesis("Quadrangle_2D", "libStdMeshersEngine.so")


algo1d_2 = smesh.CreateHypothesis("NumberOfSegments", "libStdMeshersEngine.so")
algo1d_2.SetNumberOfSegments(200)
algo1d_3 = smesh.CreateHypothesis("NumberOfSegments", "libStdMeshersEngine.so")
algo1d_3.SetNumberOfSegments(20)

my_edges=SubShapeAll(fff,ShapeType["EDGE"])
i=0
for edg in my_edges:
    i=i+1
    addToStudy(edg,"myedg_"+str(i))
    updateStudy()

my_faces=SubShapeAll(fff,ShapeType["FACE"])
i=0
for edg in my_faces:
    i=i+1
    addToStudy(edg,"myfac_"+str(i))
    updateStudy()

for tool in [hyp1d, hyp2dq, algo1d]:
    mesh2d.AddHypothesis(fff, tool)
    pass

mesh2d.AddHypothesis(my_edges[0],hyp1d_2)
mesh2d.AddHypothesis(my_edges[0],algo1d_2)


mesh2d.AddHypothesis(my_faces[0],hyp1d)
mesh2d.AddHypothesis(my_faces[0],algo1d_3)
mesh2d.AddHypothesis(my_faces[0],hyp2d)
mesh2d.AddHypothesis(my_faces[0],algo2d)

b = smesh.Compute(mesh2d, fff)
if in_tui:
    smeshgui = salome.ImportComponentGUI("SMESH")
    smeshgui.Init(salome.myStudyId)
    smeshgui.SetMeshIcon(salome.ObjectToID(mesh2d), b )
    pass

updateStudy()

file_name = "f3c_tetra.med"
from os import system
system("rm -f %s > /dev/null 2>&1"%(file_name))
file_name="/home/edmondo/Documents/DOWN/f3c_tetra.med"
mesh2d.ExportMED(file_name, 0)


