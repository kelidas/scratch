#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = LogNormal(1.5, 2.5, -1.5)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = LogNormalFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_LogNormalFactory.py", sys.exc_type, sys.exc_value
