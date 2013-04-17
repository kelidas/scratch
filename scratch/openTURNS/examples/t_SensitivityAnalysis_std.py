#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :

    RandomGenerator.SetSeed(0)
    inputDimension = 3
    outputDimension = 1

    inputName = Description(inputDimension)
    inputName[0] = "X1"
    inputName[1] = "X2"
    inputName[2] = "X3"
    outputName = Description(outputDimension)
    outputName[0] = "Y"
    formula = Description(outputDimension)
    formula[0] = "sin(_pi*X1)+7*sin(_pi*X2)*sin(_pi*X2)+0.1*((_pi*X3)*(_pi*X3)*(_pi*X3)*(_pi*X3))*sin(_pi*X1)"

    model = NumericalMathFunction(inputName, outputName, formula)

    marginals = DistributionCollection()
    marginals.add(Distribution(Uniform(-1.0,1.0)))
    #marginals[0].setDescription("Marginal 1");
    marginals.add(Distribution(Uniform(-1.0,1.0)))
    #marginals[0].setDescription("Marginal 2");
    marginals.add(Distribution(Uniform(-1.0,1.0)))
    #marginals[0].setDescription("Marginal 3");
    maDistribution = Distribution(ComposedDistribution(marginals,Copula(IndependentCopula(inputDimension))))

    size = 10000
    sample1 = maDistribution.getNumericalSample(size)
    sample2 = maDistribution.getNumericalSample(size)

    #for i in range(size):
        #for j in range(dimension):
            #sample1[i][j] = (i-0.75)/size
            #sample2[i][j] = (i-0.25)/size


    sensitivityAnalysis = SensitivityAnalysis(sample1, sample2, model)
    firstOrderIndices = sensitivityAnalysis.getFirstOrderIndices()
    totalOrderIndices = sensitivityAnalysis.getTotalOrderIndices()

    print "First order Sobol indice of Y|X1 = ", firstOrderIndices[0]
    print "Total order Sobol indice of Y|X3 = ", totalOrderIndices[2]

except :
    import sys
    print "t_SensitivityAnalysis_std.py", sys.exc_type, sys.exc_value

