#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    # We create a distribution
    distribution = Distribution(Normal())

    print "distribution = " , distribution

    aCollection = DistributionCollection(0)
    aCollection.add(Distribution(Normal(0.0, 1.0)))
    aCollection.add(Distribution(Uniform(1.0, 1.5)))
    distributionParameters = ComposedDistribution(aCollection)
    randomParameters = RandomVector(Distribution(distributionParameters))

    print "random parameters=", randomParameters
    
    # We create a distribution-based conditional RandomVector
    vect = ConditionalRandomVector(Distribution(distribution), randomParameters)
    print "vect=" , vect

    # Check standard methods of class RandomVector
    print "vect dimension=" , vect.getDimension()
    p = NumericalPoint()
    r = vect.getRealization(p)
    print "vect realization=", repr(r)
    print "parameters value=", repr(p)
    distribution.setParametersCollection(p)
    RandomGenerator().SetSeed(0)
    # Generate a parameter set to put the random generator into the proper state
    randomParameters.getRealization()
    # The realization of the distribution should be equal to the realization of the conditional vector
    print "dist realization=", repr(distribution.getRealization())
    
    print "vect sample =" , repr(vect.getNumericalSample(5))

except :
    import sys
    print "t_RandomVector_conditional.py", sys.exc_type, sys.exc_value

