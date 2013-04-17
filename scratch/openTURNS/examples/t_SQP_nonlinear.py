#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()

def printNumericalPoint(point, digits) :
  oss = "["
  eps = pow(0.1, digits)
  for i in range(point.getDimension()) :
    if i == 0 :
      sep = ""
    else :
      sep = ","
    if fabs(point[i]) < eps :
      oss += sep + "%.6f" % point[i]
    else :
      oss += sep + "%.6f" % point[i]
    sep = ","
  oss += "]"
  return oss

#TESTPREAMBLE()

try :
  try :
    # Test function operator ()
    levelFunction = NumericalMathFunction("TestOptimNonLinear")
    # Add a finite difference gradient to the function,
    # needs it
    myGradient = NonCenteredFiniteDifferenceGradient(1e-7, levelFunction.getEvaluationImplementation())
    # Substitute the gradient
    levelFunction.setGradientImplementation(NonCenteredFiniteDifferenceGradient(myGradient))
    specific = SQPSpecificParameters()
    startingPoint = NumericalPoint(4, 0.0)
    mySQPAlgorithm = SQP(specific, levelFunction)
    mySQPAlgorithm.setStartingPoint(startingPoint)
    mySQPAlgorithm.setLevelValue(-0.5)
    print "mySQPAlgorithm=", mySQPAlgorithm
    mySQPAlgorithm.run()
    print "result = ", printNumericalPoint(NearestPointAlgorithm(mySQPAlgorithm).getResult().getMinimizer(), 4)
  except :
    raise
except :
  import sys
  print "t_SQP_nonlinear.py", sys.exc_type, sys.exc_value
