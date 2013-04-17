#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Rayleigh(2.5, -1.0)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = RayleighFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
    import sys
    print "t_RayleighFactory.py", sys.exc_type, sys.exc_value
