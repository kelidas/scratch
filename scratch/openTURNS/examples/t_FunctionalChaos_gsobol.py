#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

def sobol(indice, ai):
    val = 1.0
    for i in range(indice.getSize()):
        val = val * 1.0 / (3.0 * (1.0 + ai[indice[i]])**2.0)
    return val

try :
    # Problem parameters
    dimension = 5

    # Create the Ishigami function
    # Reference analytical values
    meanTh = 1.0
    covTh = 1.0
    a = NumericalPoint(dimension)
    inputVariables = Description(dimension)
    outputVariables = Description(1)
    outputVariables[0] = "y"
    formula = Description(1)
    formula[0] = "1.0"
    for i in range(dimension):
        a[i] = 0.5 * i
        covTh = covTh * (1.0 + 1.0 / (3.0 * (1.0 + a[i])**2))
        inputVariables[i] = "xi"+str(i)
        formula[0] = formula[0] + " * ((abs(4.0 * xi" + str(i) + " - 2.0) + " + str(a[i]) + ") / (1.0 + " + str(a[i]) + "))"
    covTh = covTh - 1.0

    model = NumericalMathFunction(inputVariables, outputVariables, formula)
    # Create the input distribution
    marginals = DistributionCollection(dimension)
    for i in range(dimension):
        marginals[i] = Distribution(Uniform(0.0, 1.0))
    distribution = Distribution(ComposedDistribution(marginals))

    # Create the orthogonal basis
    polynomialCollection = PolynomialFamilyCollection(dimension)
    for i in range(dimension):
        polynomialCollection[i] = OrthogonalUniVariatePolynomialFamily(LegendreFactory())
    enumerateFunction = EnumerateFunction(dimension)
    productBasis = OrthogonalBasis(OrthogonalProductPolynomialFactory(polynomialCollection, enumerateFunction))

    # Create the adaptive strategy
    # We can choose amongst several strategies
    # First, the most efficient (but more complex!) strategy
    listAdaptiveStrategy = list()
    indexMax = 200
    basisDimension = 20
    threshold = 1.0e-6
    listAdaptiveStrategy.append(AdaptiveStrategy(CleaningStrategy(productBasis, indexMax, basisDimension, threshold, False)))
    # Second, the most used (and most basic!) strategy
    degree = 6
    listAdaptiveStrategy.append(AdaptiveStrategy(FixedStrategy(productBasis, enumerateFunction.getStrateCumulatedCardinal(degree))))
    # Third, a slight enhancement with respect to the basic strategy
    degree = 3
    listAdaptiveStrategy.append(AdaptiveStrategy(SequentialStrategy(productBasis, enumerateFunction.getStrateCumulatedCardinal(degree), False)))

    for adaptiveStrategyIndex in range(len(listAdaptiveStrategy)):
        adaptiveStrategy = listAdaptiveStrategy[adaptiveStrategyIndex]
        # Create the projection strategy
        samplingSize = 250
        listProjectionStrategy = list()
        # We have only the LeastSquaresStrategy up to now (0.13.0) but we can choose several sampling schemes
        # Monte Carlo sampling
        listProjectionStrategy.append(ProjectionStrategy(LeastSquaresStrategy(MonteCarloExperiment(samplingSize))))
        # LHS sampling
        listProjectionStrategy.append(ProjectionStrategy(LeastSquaresStrategy(LHSExperiment(samplingSize))))
        # Low Discrepancy sequence
        listProjectionStrategy.append(ProjectionStrategy(LeastSquaresStrategy(LowDiscrepancyExperiment(LowDiscrepancySequence(SobolSequence()),samplingSize))))
        for projectionStrategyIndex in range(len(listProjectionStrategy)):
            projectionStrategy = listProjectionStrategy[projectionStrategyIndex]
            # Create the polynomial chaos algorithm
            maximumResidual = 1.0e-10
            algo = FunctionalChaosAlgorithm(model, distribution, adaptiveStrategy, projectionStrategy)
            algo.setMaximumResidual(maximumResidual)
            RandomGenerator.SetSeed(0)
            algo.run()

            # Examine the results
            result = FunctionalChaosResult(algo.getResult())
            print "###################################"
            print adaptiveStrategy
            print projectionStrategy
            #print "coefficients=", result.getCoefficients()
            residual = result.getResidual()
            print "residual=%.4f" % residual

            # Post-process the results
            vector = FunctionalChaosRandomVector(result)
            mean = vector.getMean()[0]
            print "mean=%.8f" % mean, "absolute error=%.8f" % fabs(mean - meanTh)
            variance = vector.getCovariance()[0, 0]
            print "variance=%.8f" % variance, "absolute error=%.8f" % fabs(variance - covTh)
            indices = Indices(1)
            for i in range(dimension):
                indices[0] = i
                value = vector.getSobolIndex(i)
                print "Sobol index", i, "= %.8f" % value, "absolute error=%.8f" % fabs(value - sobol(indices, a))
            indices = Indices(2)
            k = 0
            for i in range(dimension):
                indices[0] = i
                for j in range(i+1, dimension):
                    indices[1] = j
                    value = vector.getSobolIndex(indices)
                    print "Sobol index", indices, "=%.8f" % value, "absolute error=%.8f" % fabs(value - sobol(indices, a))
                    k = k+1
            indices = Indices(3)
            indices[0] = 0
            indices[1] = 1
            indices[2] = 2
            value = vector.getSobolIndex(indices)
            print "Sobol index", indices, "=%.8f" % value, "absolute error=%.8f" % fabs(value - sobol(indices, a))
    
except : 
   import sys
   print "t_FunctionalChaos_ishigami.py", sys.exc_type, sys.exc_value
