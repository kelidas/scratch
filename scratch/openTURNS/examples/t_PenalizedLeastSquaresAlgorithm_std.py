#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    dimension = 2
    inVar = Description(dimension)
    inVar[0] = "x1"
    inVar[1] = "x2"
    outVar = Description(1)
    outVar[0] = "y"
    formula = Description(1)
    formula[0] = "x1^3+1.5*x2^3-x1*x2"
    model = NumericalMathFunction(inVar, outVar, formula)
    basis = NumericalMathFunctionCollection(4)
    formula[0] = "x1"
    basis[0] = NumericalMathFunction(inVar, outVar, formula)
    formula[0] = "x2"
    basis[1] = NumericalMathFunction(inVar, outVar, formula)
    formula[0] = "x1^2"
    basis[2] = NumericalMathFunction(inVar, outVar, formula)
    formula[0] = "x2^2"
    basis[3] = NumericalMathFunction(inVar, outVar, formula)
    size = 5
    inputSample = NumericalSample(size * size, dimension)
    weight = NumericalPoint(inputSample.getSize(), 1)
    for i in range(inputSample.getSize()) :
      inputSample[i][0] = float(i % size) / size
      inputSample[i][1] = float(i / size) / size
      weight[i] = (i % size + 1) * (i / size + 1)
    penalizationFactor = 0.25
    # Uniform weight, no penalization
    algo = PenalizedLeastSquaresAlgorithm(inputSample, model(inputSample), NumericalPoint(inputSample.getSize(), 1.0), basis)
    print "Uniform weight, no penalization"
    print "Coefficients=", (algo.getCoefficients())
    print "Residual=", algo.getResidual()
    # Uniform weight, spherical penalization
    algo = PenalizedLeastSquaresAlgorithm(inputSample, model(inputSample), NumericalPoint(inputSample.getSize(), 1.0), basis, penalizationFactor)
    print "Uniform weight, spherical penalization"
    print "Coefficients=", (algo.getCoefficients())
    print "Residual=", algo.getResidual()
    # Non uniform weight, spherical penalization
    algo = PenalizedLeastSquaresAlgorithm(inputSample, model(inputSample), weight, basis)
    print "Non uniform weight, no penalization"
    print "Coefficients=", (algo.getCoefficients())
    print "Residual=", algo.getResidual()
    algo = PenalizedLeastSquaresAlgorithm(inputSample, model(inputSample), weight, basis, penalizationFactor)
    print "Non uniform weight, spherical penalization"
    print "Coefficients=", (algo.getCoefficients())
    print "Residual=", algo.getResidual()
    penalizationMatrix = CovarianceMatrix(4)
    for i in range(4):
        penalizationMatrix[i, i] = 1.0
    for i in range(3):
        penalizationMatrix[i, i + 1] = 1.0/8.0
    algo = PenalizedLeastSquaresAlgorithm(inputSample, model(inputSample), weight, basis, penalizationFactor, penalizationMatrix)
    print "Non uniform weight, non spherical penalization"
    print "Coefficients=", (algo.getCoefficients())
    print "Residual=", algo.getResidual()
except :
  import sys
  print "t_PenalizedLeastSquaresAlgorithm_std.py", sys.exc_type, sys.exc_value

