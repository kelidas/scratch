#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Laplace(2.5, -1.3)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = LaplaceFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_LaplaceFactory.py", sys.exc_type, sys.exc_value
