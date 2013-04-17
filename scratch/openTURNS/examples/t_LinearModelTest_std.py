#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
  size = 100
  dim = 10
  R = CorrelationMatrix(dim)
  for i in range(dim) :
      for j in range(i) :
	  R[i, j] = (i + j + 1.0) / (2.0 * dim)
          
  mean = NumericalPoint(dim, 2.0)
  sigma = NumericalPoint(dim, 3.0)
  distribution = Normal(mean, sigma, R)
  
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
  print "LMAdjustedRSquared=", LinearModelTest.LMAdjustedRSquared(sampleY, sampleZ)
  print "LMFisher=", LinearModelTest.LMFisher(sampleY, sampleZ)
  print "LMResidualMean=", LinearModelTest.LMResidualMean(sampleY, sampleZ)
  print "LMRSquared=", LinearModelTest.LMRSquared(sampleY, sampleZ)

except :
  import sys
  print "t_LinearModelTest_std.py", sys.exc_type, sys.exc_value
