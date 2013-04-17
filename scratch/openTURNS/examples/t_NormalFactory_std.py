#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    dim = 3
    mean = NumericalPoint(dim)
    sigma = NumericalPoint(dim)
    R = CorrelationMatrix(dim)
    for i in range(dim) :
        mean[i] = i + 0.5
        sigma[i] = 2 * i + 1.0
        for j in range(i) :
            R[i, j] = 0.5 * (1.0 + i) / dim
    distribution = Normal(mean, sigma, R)
    size = 10000
    sample = distribution.getNumericalSample(size)
    factory = NormalFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "distribution=", distribution
    print "Estimated distribution=", estimatedDistribution

except :
    import sys
    print "t_NormalFactory.py", sys.exc_type, sys.exc_value
