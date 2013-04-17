#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    distribution = Normal(4)
    size = 10
    weightingDistribution = Normal(distribution)
    weightingDistribution.setMean(NumericalPoint(4, 1.0))
    myPlane = ImportanceSamplingExperiment(Distribution(distribution), Distribution(weightingDistribution), size)
    print "myPlane = ", myPlane
    sample = NumericalSample(myPlane.generate())
    print "sample = ", repr(sample)
except :
    import sys
    print "t_ImportanceSamplingExperiment_std.py", sys.exc_type, sys.exc_value
