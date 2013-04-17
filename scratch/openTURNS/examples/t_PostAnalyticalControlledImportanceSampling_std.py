#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :

    # We create a numerical math function
    myFunction = NumericalMathFunction("poutre")

    dim = myFunction.getInputDimension()

    # We create a normal distribution point of dimension 1
    mean = NumericalPoint(dim, 0.0)
    # E
    mean[0] = 50.0
    # F
    mean[1] =  1.0
    # L
    mean[2] = 10.0
    # I
    mean[3] =  5.0
    sigma = NumericalPoint(dim, 1.0)
    R = IdentityMatrix(dim)
    myDistribution = Normal(mean, sigma, R)

    # We create a 'usual' RandomVector from the Distribution
    vect = RandomVector(myDistribution)

    # We create a composite random vector
    output = RandomVector(myFunction, vect)

    # We create an Event from this RandomVector
    myEvent = Event(output, ComparisonOperator(Less()), -3)

    # We create a FORM algorithm
    # The first parameter is a NearestPointAlgorithm
    # The second parameter is an event
    # The third parameter is a starting point for the design point research
    myAlgo = FORM(NearestPointAlgorithm(Cobyla()), myEvent, mean)

    # Perform the simulation
    myAlgo.run()

    # Create a PostAnalyticalControlledImportanceSampling algorithm based on the previous FORM result
    formResult = myAlgo.getResult()
    mySamplingAlgo = PostAnalyticalControlledImportanceSampling(formResult)
    print "FORM probability=", formResult.getEventProbability()
    mySamplingAlgo.setMaximumOuterSampling(250)
    mySamplingAlgo.setBlockSize(4)
    mySamplingAlgo.setMaximumCoefficientOfVariation(0.1)

    print "PostAnalyticalControlledImportanceSampling=", mySamplingAlgo

    mySamplingAlgo.run()

    # Stream out the result
    print "PostAnalyticalControlledImportanceSampling result=", mySamplingAlgo.getResult()

    # Analyse the input sample
    inputSample = mySamplingAlgo.getInputStrategy().getSample()
    print "Input sample size=", inputSample.getSize(), " dimension=", inputSample.getDimension(), " first=", repr(inputSample[0]), " last=", repr(inputSample[inputSample.getSize()-1])
    outputSample = mySamplingAlgo.getOutputStrategy().getSample()
    print "Output sample size=", outputSample.getSize(), " dimension=", outputSample.getDimension(), " first=", repr(outputSample[0]), " last=", repr(outputSample[outputSample.getSize()-1])
except :
    import sys
    print "t_PostAnalyticalControlledImportanceSampling_std.py", sys.exc_type, sys.exc_value
