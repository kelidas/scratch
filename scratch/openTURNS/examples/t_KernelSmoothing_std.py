#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    # Instanciate one distribution object
    dim = 2
    meanPoint = NumericalPoint(dim, 1.0)
    meanPoint[0] = 0.5
    meanPoint[1] = -0.5
    sigma = NumericalPoint(dim, 1.0)
    sigma[0] = 2.0
    sigma[1] = 3.0
    R = CorrelationMatrix(dim)
    for i in range(1,dim) :
        R [i, i - 1] = 0.5

    distribution = Normal(meanPoint, sigma, R)
    discretization = 100
    kernel = KernelSmoothing()
    sample = distribution.getNumericalSample(discretization)
    kernels = DistributionCollection(0)
    kernels.add(Distribution(Normal()))
    kernels.add(Distribution(Epanechnikov()))
    kernels.add(Distribution(Uniform()))
    kernels.add(Distribution(Triangular()))
    kernels.add(Distribution(Logistic()))
    kernels.add(Distribution(Beta(2.0, 4.0, -1.0, 1.0)))
    kernels.add(Distribution(Beta(3.0, 6.0, -1.0, 1.0)))
    meanExact = distribution.getMean()
    covarianceExact = distribution.getCovariance()
    for i in range(kernels.getSize()):
        kernel = kernels[i]
        print "kernel=", kernel.getName()
        smoother = KernelSmoothing(kernel)
        smoothed = smoother.buildImplementation(sample)
        bw = smoother.getBandwidth()
        print "kernel bandwidth=[" , bw[0], ", ", bw[1], "]"
        meanSmoothed = smoothed.getMean()
        print "mean(smoothed)=[", meanSmoothed[0], ", ", meanSmoothed[1], "] mean(exact)=[", meanExact[0], ", ", meanExact[1], "]"
        covarianceSmoothed = smoothed.getCovariance()
        print "covariance=", repr(covarianceSmoothed), " covariance(exact)=", repr(covarianceExact)
        # Define a point
        point = NumericalPoint( smoothed.getDimension(), 0.0 )

        # Show PDF and CDF of point point
        pointPDF = smoothed.computePDF( point )
        pointCDF = smoothed.computeCDF( point )
        print "Point= " , repr(point)
        print " pdf(smoothed)=%.6f" % pointPDF
        print " pdf(exact)=%.6f" % distribution.computePDF( point )
        print " cdf(smoothed)=%.6f" % pointCDF
        print " cdf(exact)=%.6f" % distribution.computeCDF( point )

    # Test for boundary correction
    distributionCollection = DistributionCollection(2)
    distributionCollection[0] = Distribution(Normal(0.0, 1.0))
    distributionCollection[1] = Distribution(Beta(0.7, 1.6, -1.0, 2.0))
    sampleCollection = [distributionCollection[0].getNumericalSample(discretization), distributionCollection[1].getNumericalSample(discretization)]
    bounded = [False, True]
    for i in range(kernels.getSize()):
        kernel = Distribution(kernels[i])
        print "kernel=", kernel.getName()
        smoother = KernelSmoothing(kernel)
        for j in range(2):
            for k in range(2):
                smoothed = smoother.buildImplementation(sampleCollection[j], bounded[k])
                print "Bounded underlying distribution? ", j == 1, " bounded reconstruction? ", k == 1
                # Define a point
                point = NumericalPoint( smoothed.getDimension(), -0.9 )

                # Show PDF and CDF of point point
                pointPDF = smoothed.computePDF( point )
                pointCDF = smoothed.computeCDF( point )
                print " pdf(smoothed)= ", pointPDF, " pdf(exact)=", distributionCollection[j].computePDF( point )
                print " cdf(smoothed)= ", pointCDF, " cdf(exact)=", distributionCollection[j].computeCDF( point )

except :
    import sys
    print "t_KernelSmoothing_std.py", sys.exc_type, sys.exc_value
