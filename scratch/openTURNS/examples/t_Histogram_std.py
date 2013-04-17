#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :
    # Instanciate one distribution object
    print "begin histo comp test"
    collection = HistogramPairCollection( ((0.5, 1.0 ), (1.5, 0.7), (3.5, 1.2), (2.5, 0.9)) )
    collectionSize = len( collection )
    print "collection = ", collection
    distribution = Histogram(-1.5, collection)
    print "Distribution " , distribution

    # Is this distribution elliptical ?
    print "Elliptical = ", distribution.isElliptical()

    # Is this distribution continuous ?
    print "Continuous = ", distribution.isContinuous()

    # Test for realization of distribution
    oneRealization = distribution.getRealization()
    print "oneRealization=", repr(oneRealization)

    # Test for sampling
    size = 10000
    oneSample = distribution.getNumericalSample( size )
    print "oneSample first=" , repr(oneSample[0]) , " last=" , repr(oneSample[1])
    print "mean=" , repr(oneSample.computeMean())
    print "covariance=" , repr(oneSample.computeCovariance())

    # Define a point
    point = NumericalPoint( distribution.getDimension(), 1.0 )
    print "Point= " , repr(point)

    # Show PDF and CDF at point
    eps = 1e-5
    # derivative of PDF with regards its arguments
    DDF = distribution.computeDDF( point )
    print "ddf     =" , repr(DDF)
    # by the finite difference technique
    print "ddf (FD)=" , repr(NumericalPoint(1, (distribution.computePDF( point + NumericalPoint(1, eps) ) - distribution.computePDF( point  + NumericalPoint(1, -eps) )) / (2.0 * eps)))

    # PDF value
    PDF = distribution.computePDF( point )
    print "pdf     =%.6f" % PDF
    # by the finite difference technique from CDF
    print "pdf (FD)=%.6f" % ((distribution.computeCDF( point + NumericalPoint(1, eps) ) - distribution.computeCDF( point  + NumericalPoint(1, -eps) )) / (2.0 * eps))

    # derivative of the PDF with regards the parameters of the distribution
    CDF = distribution.computeCDF( point )
    print "cdf=%.6f" % CDF
    PDFgr = distribution.computePDFGradient( point )
    print "pdf gradient     =" , repr(PDFgr)
    # by the finite difference technique
    PDFgrFD = NumericalPoint(1 + 2 * collectionSize)
    PDFgrFD[0] = (Histogram(distribution.getFirst() + eps, distribution.getPairCollection()).computePDF(point) - Histogram(distribution.getFirst() - eps, distribution.getPairCollection()).computePDF(point)) / (2.0 * eps)
    for i in range(collectionSize) :
        collectionLeft = distribution.getPairCollection()
        collectionRight = distribution.getPairCollection()
        collectionLeft[i].h_  += eps
        collectionRight[i].h_ -= eps
        PDFgrFD[2 * i + 1] = (Histogram(distribution.getFirst(), collectionLeft).computePDF(point) - Histogram(distribution.getFirst(), collectionRight).computePDF(point)) / (2.0 * eps)
        collectionLeft = distribution.getPairCollection()
        collectionRight = collectionLeft
        collectionLeft[i].l_  += eps
        collectionRight[i].l_ -= eps
        PDFgrFD[2 * i + 2] = (Histogram(distribution.getFirst(), collectionLeft).computePDF(point) - Histogram(distribution.getFirst(), collectionRight).computePDF(point)) / (2.0 * eps)
    print "pdf gradient (FD)=" , repr(PDFgrFD)

    # derivative of the PDF with regards the parameters of the distribution
    CDFgr = distribution.computeCDFGradient( point )
    print "cdf gradient     =" , repr(CDFgr)
    # by the finite difference technique
    CDFgrFD = NumericalPoint(1 + 2 * collectionSize)
    CDFgrFD[0] = (Histogram(distribution.getFirst() + eps, distribution.getPairCollection()).computeCDF(point) - Histogram(distribution.getFirst() - eps, distribution.getPairCollection()).computeCDF(point)) / (2.0 * eps)
    for i in range(collectionSize) :
        collectionLeft = distribution.getPairCollection()
        collectionRight = distribution.getPairCollection()
        collectionLeft[i].h_  += eps
        collectionRight[i].h_ -= eps
        CDFgrFD[2 * i + 1] = (Histogram(distribution.getFirst(), collectionLeft).computeCDF(point) -
                                Histogram(distribution.getFirst(), collectionRight).computeCDF(point)) / (2.0 * eps)
        collectionLeft = distribution.getPairCollection()
        collectionRight = collectionLeft
        collectionLeft[i].l_  += eps
        collectionRight[i].l_ -= eps
        CDFgrFD[2 * i + 2] = (Histogram(distribution.getFirst(), collectionLeft).computeCDF(point) - Histogram(distribution.getFirst(), collectionRight).computeCDF(point)) / (2.0 * eps)
    print "cdf gradient (FD)=" , repr(CDFgrFD)

    # quantile
    quantile = distribution.computeQuantile( 0.95 )
    print "quantile=" , repr(quantile)
    print "cdf(quantile)=%.6f" % distribution.computeCDF(quantile)
    mean = distribution.getMean()
    print "mean=" , repr(mean)
    covariance = distribution.getCovariance()
    print "covariance=" , repr(covariance)
    parameters = distribution.getParametersCollection()
    print "parameters=" , repr(parameters)
    testSize = 0
    for i in range(testSize):
        q = RandomGenerator().Generate()
        if (fabs(q - distribution.computeCDF(distribution.computeQuantile(q))) > eps) :
            print "q=%.6f" % q ,  " quantile=%.6f" % distribution.computeQuantile(q)[0] ,  " CDF(quantile)=%.6f" % distribution.computeCDF(distribution.computeQuantile(q))

except :
    import sys
    print "t_Histogram.py", sys.exc_type, sys.exc_value

