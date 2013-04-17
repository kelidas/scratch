#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Triangular(1., 2.5, 4.0)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = TriangularFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
    import sys
    print "t_TriangularFactory.py", sys.exc_type, sys.exc_value
