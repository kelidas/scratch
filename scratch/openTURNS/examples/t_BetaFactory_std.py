#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = Beta(0.2, 0.6, -1.0, 2.0)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = BetaFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution
    distribution = Beta(0.5, 1.3, -1.0, 2.0)
    sample = distribution.getNumericalSample(size)
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution
    distribution = Beta(0.5, 2.3, -1.0, 2.0)
    sample = distribution.getNumericalSample(size)
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution
    distribution = Beta(1.5, 4.3, -1.0, 2.0)
    sample = distribution.getNumericalSample(size)
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_BetaFactory.py", sys.exc_type, sys.exc_value
