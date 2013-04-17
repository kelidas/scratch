#! /usr/bin/env python.exe

from openturns import *
Log.Show(Log.ALL)
TESTPREAMBLE()

try :

  #Instance creation
  deviation = NumericalMathFunction("poutre_external")

  inPoint = NumericalPoint(4)
  inPoint[0] = 210.e9
  inPoint[1] = 1000
  inPoint[2] = 1.5
  inPoint[3] = 2.e-6

  outPoint = deviation( inPoint )

  print "deviation =", repr(outPoint)

except :
  import sys
  print "t_NumericalMathFunction_exec_external.py", sys.exc_type, sys.exc_value
