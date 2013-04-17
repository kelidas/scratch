#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    sample = NumericalSample(4, 3)
    sample[0][0] = 1
    sample[0][1] = 0
    sample[0][2] = 9
    sample[1][0] = 2
    sample[1][1] = 3
    sample[1][2] = 5
    sample[2][0] = 5
    sample[2][1] = 1
    sample[2][2] = 8
    sample[3][0] = 6
    sample[3][1] = 7
    sample[3][2] = 2

    print "sample=" , repr(sample)
    print "min=" , repr(sample.getMin())
    print "max=" , repr(sample.getMax())
    print "mean=" , repr(sample.computeMean())
    print "covariance=" , repr(sample.computeCovariance())
    print "standard deviation=" , repr(sample.computeStandardDeviation())
    print "standard deviation per component=" , repr(sample.computeStandardDeviationPerComponent())
    print "Pearson correlation=" , repr(sample.computePearsonCorrelation())
    print "Spearman correlation=" , repr(sample.computeSpearmanCorrelation())
    print "Kendall tau=" , repr(sample.computeKendallTau())
    print "range per component=" , repr(sample.computeRangePerComponent())
    print "median per component=" , repr(sample.computeMedianPerComponent())
    print "Variance=" , repr(sample.computeVariancePerComponent())
    print "Skewness=" , repr(sample.computeSkewnessPerComponent())
    print "Kurtosis=" , repr(sample.computeKurtosisPerComponent())
    print "Marginal 1=" , repr(sample.getMarginal(1))
    indices = Indices(2)
    indices[0] = 2
    indices[1] = 0
    print "Marginal [2, 0]=" , repr(sample.getMarginal(indices))
    prob = 0.25
    print "Quantile per component(" , prob , ")=" , repr(sample.computeQuantilePerComponent(prob))
    pointCDF = NumericalPoint(sample.getDimension(), 0.25)
    print "Empirical CDF(" , repr(pointCDF) , "=" , sample.computeEmpiricalCDF(pointCDF)
    dim = 3
    R = CorrelationMatrix(dim)
    for i in range(1,dim) :
        R[i, i - 1] = 0.25
    Rtmp = CorrelationMatrix(dim)
    for i in range(dim) :
        for j in range(i) :
            Rtmp[i, j] = 6.0 * asin(R[i, j] / 2.0) / pi
    print "Pearson correlation (exact)=" , repr(R)
    print "Spearman correlation (exact)=" , repr(Rtmp)
    size = 10000
    normal = Normal(NumericalPoint(dim, 0.0), NumericalPoint(dim, 1.0), R)
    print "Normal=" , normal
    print "covariance=" , repr(normal.getCovariance())
    normalSample = normal.getNumericalSample(size)
    print "Empirical covariance=" , repr(normalSample.computeCovariance())
    RPearson = normalSample.computePearsonCorrelation()
    print "Pearson correlation=" , repr(RPearson)
    RSpearman = normalSample.computeSpearmanCorrelation()
    print "Spearman correlation=" , repr(RSpearman)
#except TestFailed, ex :
except :
    import sys
    print "t_NumericalSample_computation.py", sys.exc_type, sys.exc_value
