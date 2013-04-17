#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

class FUNC(OpenTURNSPythonFunction):

  def __init__(self):
    OpenTURNSPythonFunction.__init__(self, 2, 1)

  def f(self, X):
    print X
    Y = [0]
    Y[0] = X[0] + X[1]
    print Y
    return Y

  def fsample(self, X):
    print X
    siz = len(X)
    dim = len(X[0])
    Y = list()
    for i in range(siz):
      Y.append([X[i][0] + X[i][1]])
    print Y
    return Y

F=FUNC()
print F.getInputDimension(), F.getOutputDimension()

print F( (10,5) )

print F( ((10,5), (6,7)) )

try :

  #Instance creation
  myFunc = NumericalMathFunction( F )

  #Copy constructor
  newFunc = NumericalMathFunction(myFunc)

  print "myFunc input dimension=", myFunc.getInputDimension()
  print "myFunc output dimension=", myFunc.getOutputDimension()

  inPt = NumericalPoint(2, 2.)
  print repr(inPt)

  outPt = myFunc ( inPt )
  print repr(outPt)

  inSample = NumericalSample(10, 2)
  for i in range(10):
    inSample[i][0] = i
    inSample[i][1] = i
  print repr(inSample)

  outSample = myFunc ( inSample )

  print repr(outSample)

except :
  import sys
  print "t_NumericalMathFunction_python.py", sys.exc_type, sys.exc_value
