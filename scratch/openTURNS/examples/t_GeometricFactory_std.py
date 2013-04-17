#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Geometric(0.7)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = GeometricFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_GeometricFactory.py", sys.exc_type, sys.exc_value
