#!/usr/bin/env python
import numpy as np
import os
import os.path
import pdb
from pylab import *
import random
import shutil
import multiprocessing
import subprocess
from subprocess import call

def getOutputName(Nvar,Nsim,Nrun,seed):
    nameB = "Errors_%04dvar_%04dsim_%04druns_%02dseed.txt"%(Nvar,Nsim,Nrun,seed)
    nameA = "Freqs_%04dvar_%04dsim_%04druns_%08dseed.txt"%(Nvar,Nsim,Nrun,seed)
    return nameA, nameB 

def run_single(TYPE, Nvar, Nsim, size, seed, phipow,inum,totnum):

    Ntrials = 1000
    plotErrors = 1
    plotSamples = 0   
    plotFreq = 1
    maxT = 8
    minT = 1e-4



    if TYPE == "COR": typenorm = 0
    elif TYPE == "AE": typenorm = 4; phipow = 2
    elif TYPE == "Phi": typenorm = 4
    elif TYPE == "PAE": typenorm = 5; phipow = 2
    elif TYPE == "PPhi": typenorm = 5
    elif TYPE == "Mm": typenorm = 6
    elif TYPE == "PMm": typenorm = 7
    elif TYPE == "mM": typenorm = 8
    elif TYPE == "PmM": typenorm = 9


    nameA, nameB = getOutputName(Nvar,Nsim,size,seed)
    if not os.path.isfile(os.path.join("Samples",nameA)):
        #command = ["SimulationTests.exe", "%d"%Nsim, "%d"%Nvar, "%d"%size, "%d"%Ntrials, "%d"%seed, "%d"%plotErrors, "%d"%plotSamples, "%d"%plotFreq, "%d"%typenorm, "2", "1", "%e"%maxT, "%e"%minT, "1", "1", "-0.5", "%e"%phipow]
        #call(command) 
        print(inum, 'out of',totnum,'running ...')
        sys.stdout.flush()
        command = "SimulationTests.exe" + " %d"%Nsim + " %d"%Nvar + " %d"%size + " %d"%Ntrials + " %d"%seed + " %d"%plotErrors + " %d"%plotSamples + " %d"%plotFreq + " %d"%typenorm + " 2" + " 1" + " %e"%maxT + " %e"%minT + " 1" + " 1" + " -0.5" + " %e"%phipow
        #os.system("start /WAIT " + command)
        with open(os.devnull, "w") as fnull:
            #p = subprocess.Popen('konsole -e ls -la', stdout=fnull, shell=True)
            p = subprocess.Popen("start " + command, stdout=subprocess.PIPE, shell=True)
            p.communicate() # ?eká na dokon?ení
        print(inum, 'out of',totnum,'finished ...')
        sys.stdout.flush()
		
		
		
if __name__=="__main__":
            

    TYPE = "mM"
    phipow = 2   
    Nrun = 100
    Nvar = 2
    Nsim = 9    

    chunksize = 10000    

    threads = 11


    if not os.path.isdir("Samples"): os.mkdir("Samples") 
	
    pool = multiprocessing.Pool(processes = threads)
    t = 0
    totnum = int(Nrun/chunksize) + (Nrun%chunksize>0)
    inum = 0
    seed = 0
    while t<Nrun:
        seed += 1
        inum += 1
        size = chunksize
        if t+size>Nrun: size = Nrun-t
        t = t+size
        #run_single(TYPE, Nvar, Nsim, size, seed, phipow,inum, totnum)
        pool.apply_async(run_single, args = (TYPE, Nvar, Nsim, size, seed, phipow,inum, totnum))
    pool.close()
    pool.join()

    TYPEX = TYPE
    if TYPE in ["Phi","PPhi"]: TYPEX += "_%03d"%phipow
	
    DATA = []
    for name in os.listdir('Samples'):
        if name.endswith('.txt') and name.startswith('Freqs_%04dvar_%04dsim'%(Nvar,Nsim)):
            n = name.split('_')
            Nvar = int(n[1].replace('var',''))
            Nsim = int(n[2].replace('sim',''))
            Ntest = int(n[3].replace('runs',''))
            if len(DATA)==0:
                DATA = np.zeros(Nsim**Nvar,dtype=int)  	
            data = np.loadtxt(os.path.join("Samples",name)).astype(int)
            DATA = DATA + data


    Ntest = np.sum(DATA)/Nsim
    np.savetxt('Freqs_%04dvar_%04dsim_%druns_%s.txt'%(Nvar,Nsim, Ntest,TYPEX),DATA, fmt = '%d')
    print(np.sum(DATA)/Nsim)

    DATA = []
    for name in os.listdir('Samples'):
        if name.endswith('.txt') and name.startswith('Errors_%04dvar_%04dsim'%(Nvar,Nsim)):
            n = name.split('_')
            Nvar = int(n[1].replace('var',''))
            Nsim = int(n[2].replace('sim',''))
            Ntest = int(n[3].replace('runs',''))
            data = np.loadtxt(os.path.join("Samples",name)).astype(float)[:,2]

            if len(DATA)==0:
                DATA = data
            else:
                DATA = np.append(DATA, data)

    Ntest = len(DATA)
    np.savetxt('Errors_%04dvar_%04dsim_%druns_%s.txt'%(Nvar,Nsim, Ntest,TYPEX),DATA, fmt = '%f')
    print(Ntest, "suboptimal", len(np.where(DATA>min(DATA)+1E-6)[0]))
