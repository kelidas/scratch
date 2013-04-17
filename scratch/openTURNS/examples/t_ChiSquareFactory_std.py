#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    distribution = ChiSquare(0.5)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = ChiSquareFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution
    distribution = ChiSquare(1.0)
    sample = distribution.getNumericalSample(size)
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution
    distribution = ChiSquare(2.5)
    sample = distribution.getNumericalSample(size)
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
  import sys
  print "t_ChiSquareFactory.py", sys.exc_type, sys.exc_value
