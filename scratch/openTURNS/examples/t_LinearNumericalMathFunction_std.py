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
    linear = Matrix(outputDimension, inputDimension)
    linear[0,0] = 1.0
    linear[1,0] = 2.0
    linear[0,1] = 3.0
    linear[1,1] = 4.0
    linear[0,2] = 5.0
    linear[1,2] = 6.0

    # myFunction = linear * (X- center) + constant
    myFunction = LinearNumericalMathFunction(center, constant, linear)
    myFunction.setName("linearFunction")
    inPoint = NumericalPoint(inputDimension)
    inPoint[0] = 7.0
    inPoint[1] = 8.0
    inPoint[2] = 9.0
    outPoint = myFunction( inPoint )
    print"myFunction=" , myFunction 
    print myFunction.getName() , "( " , repr(inPoint) , " ) = " , repr(outPoint) 
    print myFunction.getName() , ".gradient( " , repr(inPoint) , " ) = " , repr(myFunction.gradient(inPoint))
    print myFunction.getName() , ".hessian( " , repr(inPoint) , " ) = " , repr(myFunction.hessian(inPoint))

except :
    import sys
    print "t_LinearNumericalMathFunction_std.py", sys.exc_type, sys.exc_value
 
