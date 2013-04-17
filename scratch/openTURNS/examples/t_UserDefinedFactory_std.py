#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    sample = NumericalSample(3, 2)
    sample[0][0] = 1.0
    sample[0][1] = 1.5
    sample[1][0] = 2.0
    sample[1][1] = 2.5
    sample[2][0] = 3.0
    sample[2][1] = 3.5

    factory = UserDefinedFactory()
    estimatedDistribution = factory.buildImplementation(sample)
    print "sample=", repr(sample)
    print "Estimated distribution=", estimatedDistribution

except :
    import sys
    print "t_UserDefinedFactory.py", sys.exc_type, sys.exc_value
