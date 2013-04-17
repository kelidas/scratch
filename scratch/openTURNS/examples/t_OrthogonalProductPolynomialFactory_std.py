#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    dim = 3
    polynomCollection = PolynomialFamilyCollection(dim)
    polynomCollection[0] = OrthogonalUniVariatePolynomialFamily(LaguerreFactory(2.5))
    polynomCollection[1] = OrthogonalUniVariatePolynomialFamily(LegendreFactory())
    polynomCollection[2] = OrthogonalUniVariatePolynomialFamily(HermiteFactory())
    productPolynomialFactory = OrthogonalProductPolynomialFactory(polynomCollection)
    print "productPolynomialFactory = ", productPolynomialFactory
    point = NumericalPoint(dim, 0.5)
    for i in range(10):
        f = NumericalMathFunction(productPolynomialFactory.build(i))
        print "i=", i, " f(point)=", f(point)
    indices = Indices([2,2,2])
    weights = NumericalPoint()
    nodes = productPolynomialFactory.getNodesAndWeights(indices, weights)
    print "Indices=", indices
    print "Nodes=", nodes
    print "Weights=", weights
except :
    import sys
    print "t_OrthogonalProductPolynomialFactory_std.py", sys.exc_type, sys.exc_value

