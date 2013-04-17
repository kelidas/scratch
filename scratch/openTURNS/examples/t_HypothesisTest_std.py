#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
  dim = 10
  R = CorrelationMatrix(dim)
  for i in range(dim) :
    for j in range(i) :
	  R[i, j] = (i + j + 1.0) / (2.0 * dim)
  mean = NumericalPoint(dim, 2.0)
  sigma = NumericalPoint(dim, 3.0)
  distribution = Normal(mean, sigma, R)
            
  size = 100
  sample = distribution.getNumericalSample(size)
  sampleX = NumericalSample(size, dim - 1)
  sampleY = NumericalSample(size, 1)
  for i in range(size) :
     sampleY[i][0] = sample[i][0]
     for j in range(1,dim) : 
	  sampleX[i][j - 1] = sample[i][j]
          
  sampleZ = NumericalSample(size, 1)
  for i in range(size) :
      sampleZ[i][0] = sampleY[i][0] * sampleY[i][0]

  discreteSample1 = Poisson(0.1).getNumericalSample(size)
  discreteSample2 = Geometric(0.4).getNumericalSample(size)
  
  
  # ChiSquared Independance test : test if two samples (of sizes not necessarily equal) are independant ?
  # Care : discrete samples only
  # H0 = independent samples
  # p-value threshold : probability of the H0 reject zone : 1-0.90 
  # p-value : probability (test variable decision > test variable decision evaluated on the samples)
  # Test = True <=> p-value > p-value threshold
  print "ChiSquared=", HypothesisTest().ChiSquared(discreteSample1, discreteSample2, 0.90)
  print "ChiSquared2=", HypothesisTest().ChiSquared(discreteSample1, discreteSample1, 0.90)
            
  # Pearson Test : test if two gaussian samples are independent (based on the evaluation of the linear correlation coefficient)
  # H0 : independent samples (linear correlation coefficient = 0)
  # Test = True <=> independent samples (linear correlation coefficient = 0)
  # p-value threshold : probability of the H0 reject zone : 1-0.90 
  # p-value : probability (test variable decision > test variable decision evaluated on the samples)
  # Test = True <=> p-value > p-value threshold
  print "Pearson=", HypothesisTest().Pearson(sampleY, sampleZ, 0.90)

  # Smirnov Test : test if two samples (of sizes not necessarily equal) follow the same distribution
  # Care : continuous distributions only
  # H0 = same continuous distribution
  # Test = True <=> same distribution
  # p-value threshold : probability of the H0 reject zone : 1-0.90 
  # p-value : probability (test variable decision > test variable decision evaluated on the samples)
  # Test = True <=> p-value > p-value threshold
  print "Smirnov=", HypothesisTest().Smirnov(sampleY, sampleZ, 0.90)

  # Spearman Test : test if two samples have a monotonous relation
  # H0 = no monotonous relation between both samples
  # Test = True <=> no monotonous relation
  # p-value threshold : probability of the H0 reject zone : 1-0.90 
  # p-value : probability (test variable decision > test variable decision evaluated on the samples)
  # Test = True <=> p-value > p-value threshold
  print "Spearman=", HypothesisTest().Spearman(sampleY, sampleZ, 0.90)
            
except :
  import sys
  print "t_HypothesisTest_std.py", sys.exc_type, sys.exc_value
