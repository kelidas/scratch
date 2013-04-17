#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Weibull(1., 2.5, -1.0)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = WeibullFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
    import sys
    print "t_WeibullFactory.py", sys.exc_type, sys.exc_value
