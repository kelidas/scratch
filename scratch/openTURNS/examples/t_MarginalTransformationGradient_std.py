#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    coll1 = DistributionCollection(0)
    coll1.add(Distribution(Normal(1.0, 2.5)))
    coll1.add(Distribution(Gamma(1.5, 3.0)))
    pointLow = NumericalPoint(0)
    pointLow.add(coll1[0].computeQuantile(0.25)[0])
    pointLow.add(coll1[1].computeQuantile(0.25)[0])
    pointHigh = NumericalPoint(0)
    pointHigh.add(coll1[0].computeQuantile(0.75)[0])
    pointHigh.add(coll1[1].computeQuantile(0.75)[0])
    coll2 = DistributionCollection(0)
    coll2.add(Distribution(Gamma(2.5, 2.0)))
    coll2.add(Distribution(Normal(3.0, 1.5)))
    # First, check the old constructor
    evaluation = MarginalTransformationEvaluation(coll1)
    transformation = MarginalTransformationGradient(evaluation)

    print "transformation=", transformation
    print "transformation.gradient(", repr(pointLow), ")=", repr(transformation.gradient(pointLow))
    print "finite difference gradient(", repr(pointLow), ")=", repr(CenteredFiniteDifferenceGradient(1.0e-5, EvaluationImplementation(evaluation.clone())).gradient(pointLow))
    print "transformation.gradient(", repr(pointHigh), ")=", repr(transformation.gradient(pointHigh))
    print "finite difference gradient(", repr(pointHigh), ")=", repr(CenteredFiniteDifferenceGradient(1.0e-5, EvaluationImplementation(evaluation.clone())).gradient(pointHigh))
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()

    # Second, check the constructor for old inverse transformation
    evaluation = MarginalTransformationEvaluation(coll1, MarginalTransformationEvaluation.TO)
    transformation = MarginalTransformationGradient(evaluation)
    print "transformation=", transformation
    uLow = NumericalPoint(coll1.getSize(), 0.25)
    uHigh = NumericalPoint(coll1.getSize(), 0.75)
    print "transformation.gradient(", repr(uLow), ")=", repr(transformation.gradient(uLow))
    print "finite difference gradient(", repr(uLow), ")=", repr(CenteredFiniteDifferenceGradient(1.0e-5, EvaluationImplementation(evaluation.clone())).gradient(uLow))
    print "transformation.gradient(", repr(uHigh), ")=", repr(transformation.gradient(uHigh))
    print "finite difference gradient(", repr(uHigh), ")=", repr(CenteredFiniteDifferenceGradient(1.0e-5, EvaluationImplementation(evaluation.clone())).gradient(uHigh))
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()

    # Third, check the constructor for the new transformation
    evaluation = MarginalTransformationEvaluation(coll1, coll2)
    transformation = MarginalTransformationGradient(evaluation)
    print "transformation=", transformation
    print "transformation.gradient(", repr(pointLow), ")=", repr(transformation.gradient(pointLow))
    print "finite difference gradient(", repr(pointLow), ")=", repr(CenteredFiniteDifferenceGradient(1.0e-5, EvaluationImplementation(evaluation.clone())).gradient(pointLow))
    print "transformation.gradient(", repr(pointHigh), ")=", repr(transformation.gradient(pointHigh))
    print "finite difference gradient(", repr(pointHigh), ")=", repr(CenteredFiniteDifferenceGradient(1.0e-5, EvaluationImplementation(evaluation.clone())).gradient(pointHigh))
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
    
except :
    import sys
    print "t_MarginalTransformationGradient_std.py", sys.exc_type, sys.exc_value
