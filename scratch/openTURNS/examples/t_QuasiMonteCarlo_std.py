#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

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
    myEvent = Event(output, ComparisonOperator(Less()), -3.0)

    # We create a Monte Carlo algorithm
    myAlgo = QuasiMonteCarlo(myEvent)
    myAlgo.setMaximumOuterSampling(250)
    myAlgo.setBlockSize(4)

    print  "QuasiMonteCarlo=" , myAlgo

    # Perform the simulation
    myAlgo.run()

    # Stream out the result
    print  "QuasiMonteCarlo result=" , myAlgo.getResult()

    # Analyse the input sample
    inputSample = myAlgo.getInputStrategy().getSample()
    print "Input sample size=", inputSample.getSize(), "dimension=", inputSample.getDimension(), "first=", repr(inputSample[0]), "last=", repr(inputSample[inputSample.getSize()-1])
    outputSample = myAlgo.getOutputStrategy().getSample()
    print "Output sample size=", outputSample.getSize(), "dimension=", outputSample.getDimension(), "first=", repr(outputSample[0]), "last=", repr(outputSample[outputSample.getSize()-1])
except :
    import sys
    print "t_QuasiMonteCarlo_std.py", sys.exc_type, sys.exc_value
