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
    transformation = MarginalTransformationHessian(evaluation)

    print "transformation=", transformation
    print "transformation.hessian(", repr(pointLow), ")=", transformation.hessian(pointLow)
    print "finite difference hessian(", repr(pointLow), ")=", CenteredFiniteDifferenceHessian(1.0e-4, EvaluationImplementation(evaluation.clone())).hessian(pointLow)
    print "transformation.hessian(", repr(pointHigh), ")=", transformation.hessian(pointHigh)
    print "finite difference hessian(", repr(pointHigh), ")=", CenteredFiniteDifferenceHessian(1.0e-4, EvaluationImplementation(evaluation.clone())).hessian(pointHigh)
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
    
    # Second, check the constructor for old inverse transformation
    evaluation = MarginalTransformationEvaluation(coll1, MarginalTransformationEvaluation.TO)
    transformation = MarginalTransformationHessian(evaluation)
    print "transformation=", transformation
    uLow = NumericalPoint(coll1.getSize(), 0.25)
    uHigh = NumericalPoint(coll1.getSize(), 0.75)
    print "transformation.hessian(", repr(uLow), ")=", transformation.hessian(uLow)
    print "finite difference hessian(", repr(uLow), ")=", CenteredFiniteDifferenceHessian(1.0e-4, EvaluationImplementation(evaluation.clone())).hessian(uLow)
    print "transformation.hessian(", repr(uHigh), ")=", transformation.hessian(uHigh)
    print "finite difference hessian(", repr(uHigh), ")=", CenteredFiniteDifferenceHessian(1.0e-4, EvaluationImplementation(evaluation.clone())).hessian(uHigh)
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
    
    # Third, check the constructor for the new transformation
    
    evaluation = MarginalTransformationEvaluation(coll1, coll2)
    transformation = MarginalTransformationHessian(evaluation)
    print "transformation=", transformation
    print "transformation.hessian(", repr(pointLow), ")=", transformation.hessian(pointLow)
    print "finite difference hessian(", repr(pointLow), ")=", CenteredFiniteDifferenceHessian(1.0e-4, EvaluationImplementation(evaluation.clone())).hessian(pointLow)
    print "transformation.hessian(", repr(pointHigh), ")=", transformation.hessian(pointHigh)
    print "finite difference hessian(", repr(pointHigh), ")=", CenteredFiniteDifferenceHessian(1.0e-4, EvaluationImplementation(evaluation.clone())).hessian(pointHigh)
    print "input dimension=", transformation.getInputDimension()
    print "output dimension=", transformation.getOutputDimension()
    
except :
    import sys
    print "t_MarginalTransformationHessian_std.py", sys.exc_type, sys.exc_value
