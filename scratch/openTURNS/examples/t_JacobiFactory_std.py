#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try:
    jacobi = JacobiFactory(2.5, 3.5)
    for i in range(10):
        print "jacobi(", i, ")=", jacobi.build(i)
    roots = jacobi.getRoots(10)
    print "jacobi(10) roots=", repr(roots)
    weights = NumericalPoint()
    nodes = jacobi.getNodesAndWeights(10, weights)
    print "jacobi(10) nodes=", nodes, "and weights=", weights
except : 
    import sys
    print "t_JacobiFactory_std.py", sys.exc_type, sys.exc_value

        
