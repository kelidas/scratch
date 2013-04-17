#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Gamma(0.2, 1.0, 1.0)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = GammaFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

    distribution = Gamma(2.3, 1.0, 1.0)
    sample = distribution.getNumericalSample(size)
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_GammaFactory.py", sys.exc_type, sys.exc_value
