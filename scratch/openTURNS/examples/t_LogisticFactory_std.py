#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Logistic(2., 2.5)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = LogisticFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_LogisticFactory.py", sys.exc_type, sys.exc_value
