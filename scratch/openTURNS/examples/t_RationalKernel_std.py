#! /usr/bin/env python.exe
from openturns import *
TESTPREAMBLE()
try:
    #instantiate a kernel=Gaussian with sigma = 2
    kernel=RationalKernel(2)
    x=NumericalPoint(2,2)
    y=NumericalPoint(2,1)

    print " kernel ([2 2],[1 1]) = ", kernel(x,y)
    print " dkernel/dx_i([2 2],[1 1]) = ", repr(kernel.partialGradient(x,y))
    print " d2kernel/(dx_i*dx_j)([2 2],[1 1]) = ", repr(kernel.partialHessian(x,y))

    x[0]=0
    x[1]=5
    y[0]=0
    y[1]=3

    print " kernel ([0 5],[0 3]) = ", kernel(x,y)
    print " dkernel/dx_i([0 5],[0 3]) = ", repr(kernel.partialGradient(x,y))
    print " d2kernel/(dx_i*dx_j)([0 5],[0 3]) = ", repr(kernel.partialHessian(x,y))


except :
    import sys
    print "t_RationalKernel_std.py", sys.exc_type, sys.exc_value
