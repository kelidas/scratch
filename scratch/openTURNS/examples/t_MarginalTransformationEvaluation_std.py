#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    coll1 = DistributionCollection(0)
    coll1.add(Distribution(Normal(1.0, 2.5)))
    coll1.add(Distribution(Gamma(1.5, 3.0, 0.0)))
    pointLow = NumericalPoint(0)
    pointLow.add(coll1[0].computeQuantile(0.25)[0])
    pointLow.add(coll1[1].computeQuantile(0.25)[0])
    pointHigh = NumericalPoint(0)
    pointHigh.add(coll1[0].computeQuantile(0.75)[0])
    pointHigh.add(coll1[1].computeQuantile(0.75)[0])
    coll2 = DistributionCollection(0)
    coll2.add(Distribution(Gamma(2.5, 2.0, 0.0)))
    coll2.add(Distribution(Normal(3.0, 1.5)))
    # First, check the old constructor
    transformation = MarginalTransformationEvaluation(coll1)
    print "transformation=", transformation
    print "transformation(", pointLow, ")=", repr(transformation(pointLow))
    print "transformation(", pointHigh, ")=", repr(transformation(pointHigh))
    # Validation using finite difference
    eps = 1e-5
    factor = 1.0 / (2.0 * eps)
    gradientLow = Matrix(5, 2)
    gradientHigh = Matrix(5, 2)

    # dT/dp0
    coll = DistributionCollection(2)
    coll[0] = Distribution(Normal(1.0 + eps, 2.5))
    coll[1] = coll1[1]
    left = MarginalTransformationEvaluation(coll)
    coll[0] = Distribution(Normal(1.0 - eps, 2.5))
    right = MarginalTransformationEvaluation(coll)
    dTdp = (left(pointLow) - right(pointLow)) * factor
    gradientLow[0, 0] = dTdp[0]
    gradientLow[0, 1] = dTdp[1]
    dTdp = (left(pointHigh) - right(pointHigh)) * factor
    gradientHigh[0, 0] = dTdp[0]
    gradientHigh[0, 1] = dTdp[1]
    # dT/dp1
    coll = DistributionCollection(2)
    coll[0] = Distribution(Normal(1.0, 2.5 + eps))
    coll[1] = coll1[1]
    left = MarginalTransformationEvaluation(coll)
    coll[0] = Distribution(Normal(1.0, 2.5 - eps))
    right = MarginalTransformationEvaluation(coll)
    dTdp = (left(pointLow) - right(pointLow)) * factor
    gradientLow[1, 0] = dTdp[0]
    gradientLow[1, 1] = dTdp[1]
    dTdp = (left(pointHigh) - right(pointHigh)) * factor
    gradientHigh[1, 0] = dTdp[0]
    gradientHigh[1, 1] = dTdp[1]
    # dT/dp2
    coll = DistributionCollection(2)
    coll[0] = coll1[0]
    coll[1] = Distribution(Gamma(1.5 + eps, 3.0, 0.0))
    left = MarginalTransformationEvaluation(coll)
    coll[1] = Distribution(Gamma(1.5 - eps, 3.0, 0.0))
    right = MarginalTransformationEvaluation(coll)
    dTdp = (left(pointLow) - right(pointLow)) * factor
    gradientLow[2, 0] = dTdp[0]
    gradientLow[2, 1] = dTdp[1]
    dTdp = (left(pointHigh) - right(pointHigh)) * factor
    gradientHigh[2, 0] = dTdp[0]
    gradientHigh[2, 1] = dTdp[1]
    # dT/dp3
    coll = DistributionCollection(2)
    coll[0] = coll1[0]
    coll[1] = Distribution(Gamma(1.5, 3.0 + eps, 0.0))
    left = MarginalTransformationEvaluation(coll)
    coll[1] = Distribution(Gamma(1.5, 3.0 - eps, 0.0))
    right = MarginalTransformationEvaluation(coll)
    dTdp = (left(pointLow) - right(pointLow)) * factor
    gradientLow[3, 0] = dTdp[0]
    gradientLow[3, 1] = dTdp[1]
    dTdp = (left(pointHigh) - right(pointHigh)) * factor
    gradientHigh[3, 0] = dTdp[0]
    gradientHigh[3, 1] = dTdp[1]
    # dT/dp4
    coll = DistributionCollection(2)
    coll[0] = coll1[0]
    coll[1] = Distribution(Gamma(1.5, 3.0, 0.0 + eps))
    left = MarginalTransformationEvaluation(coll)
    coll[1] = Distribution(Gamma(1.5, 3.0, 0.0 - eps))
    right = MarginalTransformationEvaluation(coll)
    dTdp = (left(pointLow) - right(pointLow)) * factor
    gradientLow[4, 0] = dTdp[0]
    gradientLow[4, 1] = dTdp[1]
    dTdp = (left(pointHigh) - right(pointHigh)) * factor
    gradientHigh[4, 0] = dTdp[0]
    gradientHigh[4, 1] = dTdp[1]
    
    print "transformation    parameters gradient=", repr(transformation.parametersGradient(pointLow))
    print "finite difference parameters gradient=", repr(gradientLow)
    print "transformation    parameters gradient=", repr(transformation.parametersGradient(pointHigh))
    print "finite difference parameters gradient=", repr(gradientHigh)
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
    
    # Second, check the constructor for old inverse transformation
    transformation = MarginalTransformationEvaluation(coll1, MarginalTransformationEvaluation.TO)
    print "transformation=", transformation
    uLow = NumericalPoint(coll1.getSize(), 0.25)
    uHigh = NumericalPoint(coll1.getSize(), 0.75)
    print "transformation(", uLow, ")=", repr(transformation(uLow))
    print "transformation(", uHigh, ")=", repr(transformation(uHigh))
    # Validation using finite difference
    # dT/dp0
    coll = DistributionCollection(2)
    coll[0] = Distribution(Normal(1.0 + eps, 2.5))
    coll[1] = coll1[1]
    left = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    coll[0] = Distribution(Normal(1.0 - eps, 2.5))
    right = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    dTdp = (left(uLow) - right(uLow)) * factor
    gradientLow[0, 0] = dTdp[0]
    gradientLow[0, 1] = dTdp[1]
    dTdp = (left(uHigh) - right(uHigh)) * factor
    gradientHigh[0, 0] = dTdp[0]
    gradientHigh[0, 1] = dTdp[1]
    # dT/dp1
    coll = DistributionCollection(2)
    coll[0] = Distribution(Normal(1.0, 2.5 + eps))
    coll[1] = coll1[1]
    left = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    coll[0] = Distribution(Normal(1.0, 2.5 - eps))
    right = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    dTdp = (left(uLow) - right(uLow)) * factor
    gradientLow[1, 0] = dTdp[0]
    gradientLow[1, 1] = dTdp[1]
    dTdp = (left(uHigh) - right(uHigh)) * factor
    gradientHigh[1, 0] = dTdp[0]
    gradientHigh[1, 1] = dTdp[1]
    # dT/dp2
    coll = DistributionCollection(2)
    coll[0] = coll1[0]
    coll[1] = Distribution(Gamma(1.5 + eps, 3.0, 0.0))
    left = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    coll[1] = Distribution(Gamma(1.5 - eps, 3.0, 0.0))
    right = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    dTdp = (left(uLow) - right(uLow)) * factor
    gradientLow[2, 0] = dTdp[0]
    gradientLow[2, 1] = dTdp[1]
    dTdp = (left(uHigh) - right(uHigh)) * factor
    gradientHigh[2, 0] = dTdp[0]
    gradientHigh[2, 1] = dTdp[1]
    # dT/dp3
    coll = DistributionCollection(2)
    coll[0] = coll1[0]
    coll[1] = Distribution(Gamma(1.5, 3.0 + eps, 0.0))
    left = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    coll[1] = Distribution(Gamma(1.5, 3.0 - eps, 0.0))
    right = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    dTdp = (left(uLow) - right(uLow)) * factor
    gradientLow[3, 0] = dTdp[0]
    gradientLow[3, 1] = dTdp[1]
    dTdp = (left(uHigh) - right(uHigh)) * factor
    gradientHigh[3, 0] = dTdp[0]
    gradientHigh[3, 1] = dTdp[1]
    # dT/dp4
    coll = DistributionCollection(2)
    coll[0] = coll1[0]
    coll[1] = Distribution(Gamma(1.5, 3.0, 0.0 + eps))
    left = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    coll[1] = Distribution(Gamma(1.5, 3.0, 0.0 - eps))
    right = MarginalTransformationEvaluation(coll, MarginalTransformationEvaluation.TO)
    dTdp = (left(uLow) - right(uLow)) * factor
    gradientLow[4, 0] = dTdp[0]
    gradientLow[4, 1] = dTdp[1]
    dTdp = (left(uHigh) - right(uHigh)) * factor
    gradientHigh[4, 0] = dTdp[0]
    gradientHigh[4, 1] = dTdp[1]
      
    print "transformation    parameters gradient=", repr(transformation.parametersGradient(uLow))
    print "finite difference parameters gradient=", repr(gradientLow)
    print "transformation    parameters gradient=", repr(transformation.parametersGradient(uHigh))
    print "finite difference parameters gradient=", repr(gradientHigh)
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
    
    # Third, check the constructor for the new transformation
    transformation = MarginalTransformationEvaluation(coll1, coll2)
    print "transformation=", transformation
    print "transformation(", pointLow, ")=", repr(transformation(pointLow))
    print "transformation(", pointHigh, ")=", repr(transformation(pointHigh))
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
except :
    import sys
    print "t_MarginalTransformationEvaluation_std.py", sys.exc_type, sys.exc_value
