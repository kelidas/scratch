#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()

def printNumericalPoint(point, digits) :
  oss = "["
  eps = pow(0.1, digits)
  format = "%." + str(digits) + "f"
  for i in range(point.getDimension()) :
    if i == 0 :
      sep = ""
    else :
      sep = ","
    if fabs(point[i]) < eps :
      oss += sep + format % fabs(point[i])
    else :
      oss += sep + format % point[i]
    sep = ","
  oss += "]" 
  return oss

#TESTPREAMBLE()

try :
  levelFunction = NumericalMathFunction("TestOptimNonLinear")
  specific = CobylaSpecificParameters()
  startingPoint = NumericalPoint(4, 0.0)
  myAlgorithm = Cobyla(specific, levelFunction)
  myAlgorithm.setStartingPoint(startingPoint)
  myAlgorithm.setLevelValue(3.0)
  myAlgorithm.setMaximumIterationsNumber(100)
  myAlgorithm.setMaximumAbsoluteError(1.0e-10)
  myAlgorithm.setMaximumRelativeError(1.0e-10)
  myAlgorithm.setMaximumResidualError(1.0e-10)
  myAlgorithm.setMaximumConstraintError(1.0e-10)
  myAlgorithm.run()
  
  print "result = ", printNumericalPoint(NearestPointAlgorithm(myAlgorithm).getResult().getMinimizer(), 4) 

except :
  import sys
  print "t_Cobyla_nonlinear.py", sys.exc_type, sys.exc_value
