#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    size = 5
    dim = 6
    refSample = NumericalSample(size, dim)
    for i in range(size):
        for j in range(dim):
            refSample[i][j] = i + j
    print "ref. sample=", refSample
    myPlane = FixedExperiment(refSample)
    print "myPlane = ", myPlane
    sample = myPlane.generate()
    print "sample = ", sample

except :
    import sys
    print "t_FixedExperiment_std.py", sys.exc_type, sys.exc_value

