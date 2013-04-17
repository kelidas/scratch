#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = FrankCopula(1.5)
    size = 1000
    sample = distribution.getNumericalSample(size)
    factory = FrankCopulaFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_FrankFactory.py", sys.exc_type, sys.exc_value
