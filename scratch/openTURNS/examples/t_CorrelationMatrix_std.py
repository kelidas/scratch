#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try:
    matrix1 = CorrelationMatrix(2)
    matrix1.setName("matrix1")
    print "matrix1 = " , repr(matrix1)
except:
    import sys
    print "t_CorrelationMatrix_std.py", sys.exc_type, sys.exc_value
