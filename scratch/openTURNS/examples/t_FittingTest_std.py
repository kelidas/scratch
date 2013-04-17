#! /usr/bin/env python.exe

from openturns import *
from math import fabs

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :

  continuousDistributionCollection = DistributionCollection()
  discreteDistributionCollection = DistributionCollection()
  distributionCollection = DistributionCollection()

  beta = Beta(2.0, 3.0, 0.0, 1.0)
  distributionCollection.add(Distribution(beta))
  continuousDistributionCollection.add(Distribution(beta))

  gamma = Gamma(1.0, 2.0, 3.0)
  distributionCollection.add(Distribution(gamma))
  continuousDistributionCollection.add(Distribution(gamma))

  gumbel = Gumbel(1.0, 2.0)
  distributionCollection.add(Distribution(gumbel))
  continuousDistributionCollection.add(Distribution(gumbel))

  lognormal = LogNormal(1.0, 1.0, 2.0)
  distributionCollection.add(Distribution(lognormal))
  continuousDistributionCollection.add(Distribution(lognormal))

  logistic = Logistic(1.0, 1.0)
  distributionCollection.add(Distribution(logistic))
  continuousDistributionCollection.add(Distribution(logistic))

  normal = Normal(1.0, 2.0)
  distributionCollection.add(Distribution(normal))
  continuousDistributionCollection.add(Distribution(normal))

  truncatednormal = TruncatedNormal(1.0, 1.0, 0.0, 3.0)
  distributionCollection.add(Distribution(truncatednormal))
  continuousDistributionCollection.add(Distribution(truncatednormal))

  student = Student(10.0, 10.0)
  distributionCollection.add(Distribution(student))
  continuousDistributionCollection.add(Distribution(student))

  triangular = Triangular(-1.0, 2.0, 4.0)
  distributionCollection.add(Distribution(triangular))
  continuousDistributionCollection.add(Distribution(triangular))

  uniform = Uniform(1.0, 2.0)
  distributionCollection.add(Distribution(uniform))
  continuousDistributionCollection.add(Distribution(uniform))

  weibull = Weibull(1.0, 1.0, 2.0)
  distributionCollection.add(Distribution(weibull))
  continuousDistributionCollection.add(Distribution(weibull))

  geometric = Geometric(0.5)
  distributionCollection.add(Distribution(geometric))
  discreteDistributionCollection.add(Distribution(geometric))

  poisson = Poisson(2.0)
  distributionCollection.add(Distribution(poisson))
  discreteDistributionCollection.add(Distribution(poisson))

  collection = UserDefinedPairCollection(3, UserDefinedPair(NumericalPoint(1), 0.0))

  point = NumericalPoint(1)
  point[0] = 1.0
  collection[0] = UserDefinedPair(point, 0.3)
  point[0] = 2.0
  collection[1] = UserDefinedPair(point, 0.2)
  point[0] = 3.0
  collection[2] = UserDefinedPair(point, 0.5)
  userdefined = UserDefined(collection)
  distributionCollection.add(Distribution(userdefined))
  discreteDistributionCollection.add(Distribution(userdefined))

  size = 100

  # Number of continuous distributions
  continuousDistributionNumber = continuousDistributionCollection.getSize()
  # Number of discrete distributions
  discreteDistributionNumber = discreteDistributionCollection.getSize()
  # Number of distributions
  distributionNumber = continuousDistributionNumber + discreteDistributionNumber

  # We create a collection of NumericalSample of size "size" and of dimension 1 (scalar values) : the collection has distributionNumber NumericalSamples

  sampleCollection = [NumericalSample(size, 1) for i in range(distributionNumber)]
  # We create a collection of NumericalSample of size "size" and of dimension 1 (scalar values) : the collection has continuousDistributionNumber NumericalSamples
  continuousSampleCollection = [NumericalSample(size, 1) for i in range(continuousDistributionNumber)]
  # We create a collection of NumericalSample of size "size" and of dimension 1 (scalar values) : the collection has discreteDistributionNumber NumericalSamples
  discreteSampleCollection = [NumericalSample(size, 1) for i in range(discreteDistributionNumber)]

  for i in range(continuousDistributionNumber) :
    continuousSampleCollection[i] = continuousDistributionCollection[i].getNumericalSample(size)
    continuousSampleCollection[i].setName(continuousDistributionCollection[i].getName())
    sampleCollection[i] = continuousSampleCollection[i]
  for i in range(discreteDistributionNumber) :
    discreteSampleCollection[i] = discreteDistributionCollection[i].getNumericalSample(size)
    discreteSampleCollection[i].setName(discreteDistributionCollection[i].getName())
    sampleCollection[continuousDistributionNumber + i] = discreteSampleCollection[i]

  factoryCollection = DistributionFactoryCollection(3)
  factoryCollection[0] = DistributionFactory(UniformFactory())
  factoryCollection[1] = DistributionFactory(BetaFactory())
  factoryCollection[2] = DistributionFactory(NormalFactory())
  aSample = Uniform(-1.5, 2.5).getNumericalSample(size)
  print "best model BIC=", FittingTest().BestModelBIC(aSample, factoryCollection)
  print "best model Kolmogorov=", FittingTest().BestModelKolmogorov(aSample, factoryCollection)

  # BIC ranking
  resultBIC = SquareMatrix(distributionNumber)
  for i in range(distributionNumber) :
    for j in range(distributionNumber) :
      value = FittingTest().BIC(sampleCollection[i], distributionCollection[j], 0)
      resultBIC[i, j] = value
  print "resultBIC=" , repr(resultBIC)

  # Kolmogorov ranking
  resultKolmogorov = SquareMatrix(continuousDistributionNumber)
  for i in range(continuousDistributionNumber) :
    for j in range(continuousDistributionNumber) :
      value = FittingTest().Kolmogorov(continuousSampleCollection[i], continuousDistributionCollection[j], 0.95, 0).getPValue()
      if (fabs(value) < 1.0e-6):
        value = 0.0
      resultKolmogorov[i, j] =  value
  print "resultKolmogorov=" , repr(resultKolmogorov)

  # ChiSquared ranking
  resultChiSquared = SquareMatrix(discreteDistributionNumber - 1)
  for i in range(discreteDistributionNumber - 1) :
    for j in range(discreteDistributionNumber - 1) :
      value = FittingTest().ChiSquared(discreteSampleCollection[i], discreteDistributionCollection[j], 0.95, 0).getPValue()
      if (fabs(value) < 1.0e-6):
        value = 0.0
      resultChiSquared[i, j] = value
  print "resultChiSquared=" , repr(resultChiSquared)


except  :
  import sys
  print "t_FittingTest_std.py", sys.exc_type, sys.exc_value
