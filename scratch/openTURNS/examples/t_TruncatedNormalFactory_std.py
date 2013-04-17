#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    mu = NumericalPoint(4, 0.0)
    sigma = NumericalPoint(4, 1.0)
    a = NumericalPoint(4)
    b = NumericalPoint(4)
    a[0] = -4.0
    b[0] = 4.0
    a[1] = -1.0
    b[1] = 4.0
    a[2] = 1.0
    b[2] = 2.0
    a[3] = 3.0
    b[3] = 6.0

    PlatformInfo.SetNumericalPrecision(4)
    for i in range(4) :
        distribution = TruncatedNormal(mu[i], sigma[i], a[i], b[i])
        size = 10000
        sample = distribution.getNumericalSample(size)
        factory = TruncatedNormalFactory()
        estimatedDistribution = factory.buildImplementation(sample)
        print "distribution=", distribution
        print "Estimated distribution=", estimatedDistribution

except :
    import sys
    print "t_TruncatedNormalFactory.py", sys.exc_type, sys.exc_value
