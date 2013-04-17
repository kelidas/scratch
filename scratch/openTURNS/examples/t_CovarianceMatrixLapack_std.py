#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try:
    matrix1 = CovarianceMatrix(2)
    print "matrix1 (default)= " , repr(matrix1)
    matrix1[0,0]=1.
    matrix1[1,0]=.5
    matrix1[1,1]=1.
    print "matrix1 (initialized)= " , repr(matrix1)
    
    pt = NumericalPoint()
    pt.add(5.)
    pt.add(0.)
    print "pt = " , repr(pt)
    
    result  = NumericalPoint()
    result = matrix1.solveLinearSystem(pt)
    print "result = " , repr(result)
    
    determinant = matrix1.computeDeterminant()
    print "determinant = %.6f" % determinant
    
    ev = NumericalScalarCollection(2)
    ev = matrix1.computeEigenValues()
    print "ev = " , repr(ev)

    if   matrix1.isPositiveDefinite() :
        isSPD = "true"
    else :
        isSPD = "false"
    print "isSPD = " , isSPD

    matrix2 = matrix1.computeCholesky()
    print "matrix2 = " , repr(matrix2)
except:
    import sys
    print "t_CovarianceMatrixLapack_std.py", sys.exc_type, sys.exc_value
