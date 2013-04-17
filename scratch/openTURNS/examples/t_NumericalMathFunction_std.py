#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :

  #Instance creation
  myFunc = NumericalMathFunction("poutre")

  #Copy constructor
  newFunc = NumericalMathFunction(myFunc)

  print "myFunc="+ repr(myFunc)
  print "myFunc input parameter(s)="
  for i in range(myFunc.getInputDimension()) :
    print myFunc.getInputDescription()[i]
  print "myFunc output parameter(s)="
  for i in range(myFunc.getOutputDimension()) :
    print myFunc.getOutputDescription()[i]

except :
  import sys
  print "t_NumericalMathFunction_std.py", sys.exc_type, sys.exc_value
