#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :

  try :
      #Test function operator ()
      levelFunction = NumericalMathFunction("TestOptimLinear")
      specific = AbdoRackwitzSpecificParameters()
      startingPoint = NumericalPoint(4, 1.0)
      myAlgorithm = AbdoRackwitz(specific, levelFunction)
      myAlgorithm.setStartingPoint(startingPoint)
      myAlgorithm.setLevelValue(3.0)
      myAlgorithm.setMaximumIterationsNumber(100)
      myAlgorithm.setMaximumAbsoluteError(1.0e-10)
      myAlgorithm.setMaximumRelativeError(1.0e-10)
      myAlgorithm.setMaximumResidualError(1.0e-10)
      myAlgorithm.setMaximumConstraintError(1.0e-10)
      print "myAlgorithm = ", myAlgorithm
  # except NoWrapperFileFoundException, ex :
  except :
      raise

except :
  import sys
  print "t_AbdoRackwitz_std.py", sys.exc_type, sys.exc_value

