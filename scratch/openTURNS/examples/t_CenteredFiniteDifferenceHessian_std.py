#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    eps = 1e-2
    # Instance creation
    myFunc = NumericalMathFunction("TestResponseSurface")
    epsilon = NumericalPoint(myFunc.getInputDimension(), eps)
    inPoint = NumericalPoint(epsilon.getDimension(), 1.0)
    myHessian = CenteredFiniteDifferenceHessian(epsilon, myFunc.getEvaluationImplementation())

    print "myHessian=" , myHessian
    print "myFunc.hessian(" , repr(inPoint) , ")=" , myFunc.hessian(inPoint) 
    print "myHessian.hessian(" , repr(inPoint) , ")=" , myHessian.hessian(inPoint) 

    # Substitute the hessian 
    myFunc.setHessianImplementation(CenteredFiniteDifferenceHessian(myHessian))
    print "myFunc.hessian(" , repr(inPoint) , ")=" , myFunc.hessian(inPoint) , " (after substitution)"

except :
    import sys
    print "t_CenteredFiniteDifferenceHessian_std.py", sys.exc_type, sys.exc_value

