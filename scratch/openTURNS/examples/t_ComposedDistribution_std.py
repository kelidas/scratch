#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    PlatformInfo.SetNumericalPrecision(5)
    mean = NumericalPoint(3)
    mean[0] = 1.0
    mean[1] = 2.0
    mean[2] = 3.0
    sigma = NumericalPoint(3)
    sigma[0] = 2.0
    sigma[1] = 3.0
    sigma[2] = 4.0
    # Create a collection of distribution attente TUI
    aCollection = DistributionCollection(3)
    # Create a marginal : distribution 1D
    marginal = Normal(mean[0], sigma[0])
    marginal.setName("First")
    component = Description(1)
    component[0] = "One"
    marginal.setDescription(component)
    # Fill the first marginal of aCollection
    aCollection[0] = Distribution(marginal, "First")
    # Create a second marginal : distribution 1D
    marginal = Normal(mean[1], sigma[1])
    marginal.setName("Second")
    component[0] = "Two"
    marginal.setDescription(component)
    # Fill the second marginal of aCollection
    aCollection[1] = Distribution(marginal, "Second")
    # Create a third marginal : distribution 1D
    marginal = Normal(mean[2], sigma[2])
    marginal.setName("Third")
    component[0] = "Three"
    marginal.setDescription(component)
    # Fill the third marginal of aCollection
    aCollection[2] = Distribution(marginal, "Third")
    # Create a copula : IndependentCopula
    dim = aCollection.getSize()
    aCopula = IndependentCopula(dim)
    aCopula.setName("Independent copula")
    print "Copula = ", aCopula
    # Instanciate one distribution object
    distribution = ComposedDistribution(aCollection, Copula(aCopula))
    distribution.setName("myDist")
    print "Distribution = " , distribution
    print "Parameters = " , repr(distribution.getParametersCollection())
    print "Mean = " , repr(distribution.getMean())
    print "Covariance = " , repr(distribution.getCovariance())
    # Is this distribution elliptical ?
    print "Elliptical = ", distribution.isElliptical()
    # Has this distribution an elliptical copula?
    print "Elliptical copula = ", distribution.hasEllipticalCopula()

    # Has this distribution an independent copula?
    print "Independent copula = ",  distribution.hasIndependentCopula()

    # Test for realization of distribution
    oneRealization = distribution.getRealization()
    print "oneRealization=", repr(oneRealization)

    # Test for sampling
    size = 10
    oneSample = distribution.getNumericalSample( size )
    print "oneSample=", repr(oneSample)

    # Test for sampling
    size = 10000
    anotherSample = distribution.getNumericalSample( size )
    print "anotherSample mean=", repr(anotherSample.computeMean())
    print "anotherSample covariance=", repr(anotherSample.computeCovariance())

    # Define a point
    zero = NumericalPoint( dim, 0.0 )

    # Show PDF and CDF of zero point
    zeroPDF = distribution.computePDF( zero )
    zeroCDF = distribution.computeCDF( zero )
    print "Zero point= ", repr(zero), " pdf=%.6f" % zeroPDF, " cdf=%.6f" % zeroCDF

    # Get 95% quantile
    quantile = NumericalPoint(distribution.computeQuantile( 0.95 ))
    print "Quantile=", repr(quantile)
    print "CDF(quantile)=%.6f" % distribution.computeCDF(quantile)

    # Reference : Normal nD, correlation matrix = identity
    ref = Normal(mean, sigma,  CorrelationMatrix(dim))
    print "Reference="
    print "Zero point= " , repr(zero), " pdf= %.6f" % ref.computePDF(zero), " cdf= %.6f" % ref.computeCDF(zero)," quantile= " , repr(ref.computeQuantile(0.95))

    # Extract the marginals
    for i in range(dim) :
        margin = Distribution(Distribution(distribution).getMarginal(i))
        print "margin=", margin
        print "margin PDF=%.6f" % margin.computePDF(NumericalPoint(1))
        print "margin CDF=%.6f" % margin.computeCDF(NumericalPoint(1))
        print "margin quantile=", repr(margin.computeQuantile(0.5))
        print "margin realization=", repr(margin.getRealization())

    # Extract a 2-D marginal
    indices = Indices(2, 0)
    indices[0] = 1
    indices[1] = 0
    print "indices=", indices
    margins = Distribution(Distribution(distribution).getMarginal(indices))
    print "margins=", margins
    print "margins PDF=%.6f" % margins.computePDF(NumericalPoint(2))
    print "margins CDF=%.6f" % margins.computeCDF(NumericalPoint(2))
    quantile = NumericalPoint(margins.computeQuantile(0.5))
    print "margins quantile=", repr(quantile)
    print "margins CDF(qantile)=%.6f" % margins.computeCDF(quantile)
    print "margins realization=", repr(margins.getRealization())

##################################################################

    # With a Normal copula
    correlation = CorrelationMatrix(dim)
    for i in range(1,dim) :
        correlation[i - 1, i] = 0.25
    anotherCopula = NormalCopula(correlation)
    anotherCopula.setName("Normal copula")

    # Instanciate one distribution object
    distribution = ComposedDistribution(aCollection, Copula(anotherCopula))
    distribution.setName("myDist")
    distributionRef = Normal(mean, sigma, correlation)
    print "Distribution " , distribution
    print "Parameters " , repr(distribution.getParametersCollection())

    # Show PDF and CDF at point
    point = NumericalPoint(dim, 0.0)
    print "PDF      =", distribution.computePDF(point)
    print "PDF (ref)=", distributionRef.computePDF(point)
    print "CDF      =", distribution.computeCDF(point)
    print "CDF (ref)=", distributionRef.computeCDF(point)
    # 95% quantile
    quantile = distribution.computeQuantile( 0.95 )
    print "Quantile      =", repr(quantile)
    print "Quantile (ref)=", repr(distributionRef.computeQuantile(0.95))
    print "CDF(quantile)=", distribution.computeCDF(quantile)
    print "Mean      =" , repr(distribution.getMean())
    print "Mean (ref)=" , repr(distributionRef.getMean())
    print "Standard deviation      =" , repr(distribution.getStandardDeviation())
    print "Standard deviation (ref)=" , repr(distributionRef.getStandardDeviation())
    print "Skewness      =" , repr(distribution.getSkewness())
    print "Skewness (ref)=" , repr(distributionRef.getSkewness())
    print "Kurtosis      =" , repr(distribution.getKurtosis())
    print "Kurtosis (ref)=" , repr(distributionRef.getKurtosis())
    print "Covariance      =" , repr(distribution.getCovariance())
    print "Covariance (ref)=" , repr(distributionRef.getCovariance())
    anotherSample = distribution.getNumericalSample(size)
    print "anotherSample mean=" , repr(anotherSample.computeMean())
    print "anotherSample covariance=" , repr(anotherSample.computeCovariance())

except :
    import sys
    print "t_ComposedDistribution_std.py", sys.exc_type, sys.exc_value
