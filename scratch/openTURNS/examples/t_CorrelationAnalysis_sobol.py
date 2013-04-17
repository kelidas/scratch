#! /usr/bin/env python.exe

from openturns import *
from math import *

#TESTPREAMBLE()

try :

    dimension = 3;
    sampleSize = 1000;

    # we create an analytical function
    input = Description(dimension);
    input[0] = "x0";
    input[1] = "x1";
    input[2] = "x2";
    print "input=", input

    foutput = Description(1);
    foutput[0] = "f0";
    print "output=", foutput

    formulas = Description(foutput.getSize());
    formulas[0] = "sin(x0)+7*sin(x1)^2+0.1*x2^4*sin(x0)";

    analytical = NumericalMathFunction(input, foutput, formulas);
    print "analytical=", analytical

    # we create a collection of uniform distributions over [-Pi; Pi[
    aCollection = DistributionCollection();
    for i in range(dimension) :
        aCollection.add(Distribution(Uniform(-pi, +pi)));

    # we create an independent copula
    aCopula = IndependentCopula(aCollection.getSize());
    aCopula.setName("an independent copula");

    # we create one distribution object
    aDistribution = ComposedDistribution(aCollection, Copula(aCopula));
    aDistribution.setName("a uniform distribution");

    # we create two input samples for the function
    firstInputSample = aDistribution.getNumericalSample(sampleSize);
    secondInputSample = aDistribution.getNumericalSample(sampleSize);

    # Choose which indices to compute
    indiceParameters = CorrelationAnalysisSobolIndiceParameters();
    # Choose to compute indices until order 3 (requires computation of inferior order indices)
    indiceParameters.setMaximumOrder(3);
    # Choose to compute total order indices
    indiceParameters.setTotalIndiceComputation(True);

    # Compute the Sobol' indices
    myResult = CorrelationAnalysis.SobolIndice(indiceParameters, firstInputSample, secondInputSample, analytical);

    # Retrieve the indices from result according to the selected indices via indiceParameters
    # firstOrderIndice[i] is the first order indice of variable i
    firstOrderIndice = NumericalPoint(myResult.getFirstOrderIndice());
    # secondOrderIndice(i, j) is the second order indice for both variables i and j (i not equal to j)
    secondOrderIndice = SymmetricMatrix(myResult.getSecondOrderIndice());
    # thirdOrderIndice(i, j, k) is the indice for the subset of variables {i, j, k} (i, j and k are different)
    thirdOrderIndice = SymmetricTensor(myResult.getThirdOrderIndice());
    # totalOrder[i] is the total indice for variable i
    totalOrderIndice = NumericalPoint(myResult.getTotalOrderIndice());

    # stream out the indices
    print "first order indices=", repr(firstOrderIndice);
    print "second order indices=", repr(secondOrderIndice);
    print "third order indices=", repr(thirdOrderIndice);
    print "total order indices=", repr(totalOrderIndice);

except :
  import sys
  print "t_CorrelationAnalysis_sobol.py", sys.exc_type, sys.exc_value
