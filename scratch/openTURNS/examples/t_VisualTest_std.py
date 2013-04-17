#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()
RandomGenerator().SetSeed(0)

try :

  # Generate a Normal sample
  normal = Normal(1)
  size = 100
  sample = normal.getNumericalSample(size)
  sampleCDF = VisualTest().DrawEmpiricalCDF(sample, sample.getMin()[0] - 1.0, sample.getMax()[0] + 1.0)
  sampleCDF.draw("sampleCDF", 640, 480)
  print "bitmap = " + sampleCDF.getBitmap()
  print "postscript = " + sampleCDF.getPostscript()

  sampleCDF = VisualTest().DrawEmpiricalCDF(sample, -0.5, 0.5)
  sampleCDF.draw("sampleCDFZoom", 640, 480)
  print "bitmap = " + sampleCDF.getBitmap()
  print "postscript = " + sampleCDF.getPostscript()

  sampleHist = VisualTest().DrawHistogram(sample, 10)
  sampleHist.draw("sampleHist", 640, 480)
  print "bitmap = " + sampleHist.getBitmap()
  print "postscript = " + sampleHist.getPostscript()

  sampleHist = VisualTest().DrawHistogram(sample)
  sampleHist.draw("sampleHistOpt", 640, 480)
  print "bitmap = " + sampleHist.getBitmap()
  print "postscript = " + sampleHist.getPostscript()

  sample2 = Gamma(3.0, 4.0, 0.0).getNumericalSample(size)
  twoSamplesQQPlot = VisualTest().DrawQQplot(sample, sample2, 100)
  twoSamplesQQPlot.draw("twoSamplesQQPlot", 640, 480)
  print "bitmap = " + twoSamplesQQPlot.getBitmap()
  print "postscript = " + twoSamplesQQPlot.getPostscript()

#   OT::Base::Stat::LinearModelFactory lmfact

#   NumericalSample oneSample = beta.getNumericalSample( 20 )
#   NumericalSample twoSample = beta.getNumericalSample( 20 )
#   OT::Base::Stat::LinearModel lmtest=lmfact.buildLM(oneSample,twoSample)

#   Graph drawLMVTest(test.drawLMVisualTest(oneSample, twoSample, lmtest, 1))
#   drawLMVTest.draw("LMV", 640, 480)
#   print "bitmap = " , drawLMVTest.getBitmap()
#   print "postscript = " , drawLMVTest.getPostscript()

#   Graph drawLMRTest(test.drawLMResidualTest(oneSample, twoSample, lmtest))
#   drawLMRTest.draw("LMR", 640, 480)
#   print "bitmap = " , drawLMRTest.getBitmap()
#   print "postscript = " , drawLMRTest.getPostscript()


  sampleDistributionQQPlot = VisualTest().DrawQQplot(sample, Distribution(normal), 100)
  sampleDistributionQQPlot.draw("sampleDistributionQQPlot", 640, 480)
  print "bitmap = " + sampleDistributionQQPlot.getBitmap()
  print "postscript = " + sampleDistributionQQPlot.getPostscript()

  henryPlot = VisualTest().DrawHenryLine(sample)
  henryPlot.draw("HenryPlot", 640, 480)
  print "bitmap = " + henryPlot.getBitmap()
  print "postscript = " + henryPlot.getPostscript()


except :
  import sys
  print "t_VisualTest_std.py", sys.exc_type, sys.exc_value
