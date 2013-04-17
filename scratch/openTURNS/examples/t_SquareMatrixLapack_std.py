#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    matrix1 = SquareMatrix(2)
    matrix1[0,0]=1.
    matrix1[1,0]=2.
    matrix1[0,1]=5.
    matrix1[1,1]=12.
    print "matrix1 = " , repr(matrix1)

    pt = NumericalPoint()
    pt.add(5.)
    pt.add(0.)
    print "pt = " , repr(pt)

    result = NumericalPoint()
    result = matrix1.solveLinearSystem(pt)
    print "result = " , repr(result)

    determinant = matrix1.computeDeterminant()
    print "determinant = %.6f" % determinant

    ev = matrix1.computeEigenValues()
    print "ev = " , ev

except :
    import sys
    print "t_SquareMatrixLapack_std.py", sys.exc_type, sys.exc_value
