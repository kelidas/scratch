#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    distribution = Normal(4)
    size = 10
    myPlane = MonteCarloExperiment(Distribution(distribution), size)
    print "myPlane = ", myPlane
    sample = NumericalSample(myPlane.generate())
    print "sample = ", repr(sample)
except :
    import sys
    print "t_MonteCarloExperiment_std.py", sys.exc_type, sys.exc_value
