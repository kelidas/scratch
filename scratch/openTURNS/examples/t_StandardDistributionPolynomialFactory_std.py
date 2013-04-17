#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    iMax = 5
    distributionCollection = DistributionCollection()
    distributionCollection.add(Distribution(Laplace(1.0, 0.0)))
    distributionCollection.add(Distribution(Logistic(0.0, 1.0)))
    distributionCollection.add(Distribution(LogNormal(0.0, 1.0, 0.0)))
    distributionCollection.add(Distribution(Normal(0.0, 1.0)))
    distributionCollection.add(Distribution(Rayleigh(1.0)))
    distributionCollection.add(Distribution(Student(22)))
    distributionCollection.add(Distribution(Triangular(-1.0, 0.3, 1.0)))
    distributionCollection.add(Distribution(Uniform(-1.0,1.0)))
    distributionCollection.add(Distribution(Weibull(1.0, 3.0)))
    for n in range(distributionCollection.getSize()):
        distribution = distributionCollection[n]
        name = distribution.getImplementation().getClassName()
        polynomialFactory = StandardDistributionPolynomialFactory(distribution)
        print "polynomialFactory(", name, "=", polynomialFactory
        for i in range(iMax):
            print name, " polynomial(", i, ")=", polynomialFactory.build(i)
        roots = polynomialFactory.getRoots(iMax - 1)
        print name, " polynomial(", iMax - 1, ") roots=", roots
        weights = NumericalPoint()
        nodes = polynomialFactory.getNodesAndWeights(iMax - 1, weights)
        print name, " polynomial(", iMax - 1, ") nodes=", nodes, " and weights=", weights

except :
    import sys
    print "t_StandardDistributionPolynomialFactory_std.py", sys.exc_type, sys.exc_value

