#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try:
    # First : an n by n case
    matrix1 = Matrix(2,2)
    matrix1[0,0]=1.
    matrix1[1,0]=2.
    matrix1[0,1]=5.
    matrix1[1,1]=12.
    print "matrix1 = " + repr(matrix1)

    pt1 = NumericalPoint()
    pt1.add(5.)
    pt1.add(0.)
    print "pt1 = " + repr(pt1)

    result1  = NumericalPoint()
    result1 = matrix1.solveLinearSystem(pt1)
    print "result1 = " + repr(result1)

    # Second : an n by p case, n < p
    matrix2 = Matrix(2,3)
    matrix2[0,0]=1.
    matrix2[1,0]=2.
    matrix2[0,1]=5.
    matrix2[1,1]=12.
    matrix2[0,2]=3.
    matrix2[1,2]=4.
    print "matrix2 = " + repr(matrix2)

    pt2 = NumericalPoint()
    pt2.add(5.)
    pt2.add(0.)
    print "pt2 = " + repr(pt2)

    result2 = NumericalPoint()
    result2 = matrix2.solveLinearSystem(pt2)
    print "result2 = " + repr(result2)

    # Third : an n by p case, n > p
    matrix3 = Matrix(3,2)
    matrix3[0,0]=1.
    matrix3[1,0]=2.
    matrix3[2,0]=4.
    matrix3[0,1]=5.
    matrix3[1,1]=12.
    matrix3[2,1]=3.

    print "matrix3 = " + repr(matrix3)

    pt3 = NumericalPoint()
    pt3.add(5.)
    pt3.add(0.)
    pt3.add(1.)
    print "pt3 = " + repr(pt3)

    result3 = NumericalPoint()
    result3 = matrix3.solveLinearSystem(pt3)
    print "result3 = " + repr(result3)
except:
    import sys
    print "t_MatrixSolveLinearSystem_std.py", sys.exc_type, sys.exc_value
