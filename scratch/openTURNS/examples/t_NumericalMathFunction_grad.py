#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
  #Instance creation
  deviation = NumericalMathFunction("poutre")

  inPoint = NumericalPoint(4)
  inPoint[0] = 210.e9
  inPoint[1] = 1000
  inPoint[2] = 1.5
  inPoint[3] = 2.e-6

  gradient = deviation.gradient( inPoint )

  print "deviation.gradient = ", repr(gradient)

except :
  import sys
  print "t_NumericalMathFunction_grad.py", sys.exc_type, sys.exc_value
