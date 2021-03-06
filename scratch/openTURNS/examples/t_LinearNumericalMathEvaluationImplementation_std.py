#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    inputDimension = 3
    outputDimension = 2
    # Center
    center = NumericalPoint(inputDimension)
    center[0] = -1
    center[1] = 0.5
    center[2] = 1
    # Constant term
    constant = NumericalPoint(outputDimension)
    constant[0] = -1.0
    constant[1] =  2.0
    # Linear term
    linear = Matrix(inputDimension, outputDimension)
    linear[0,0] = 1.0
    linear[1,0] = 2.0
    linear[2,0] = 3.0
    linear[0,1] = 4.0
    linear[1,1] = 5.0
    linear[2,1] = 6.0

    # myFunction = linear * (X- center) + constant
    myFunction = LinearNumericalMathEvaluationImplementation(center, constant, linear)
    myFunction.setName("linearFunction")
    inPoint = NumericalPoint(inputDimension)
    inPoint[0] = 7.0
    inPoint[1] = 8.0
    inPoint[2] = 9.0
    outPoint = myFunction( inPoint )
    print"myFunction=" , myFunction 
    print myFunction.getName() , "( " , repr(inPoint) , " ) = " , repr(outPoint) 

#except TestFailed, ex :
except :
  import sys
  print "t__LinearNumericalMathEvaluationImplementation_std.py", sys.exc_type, sys.exc_value
 
