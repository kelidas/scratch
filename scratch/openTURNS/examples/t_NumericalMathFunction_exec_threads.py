#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    # Instance creation
    external = NumericalMathFunction("external_code_threads")

    size = 20
    dimension = external.getInputDimension()
    sample = NumericalSample(size, dimension)
    for i in range(size):
        for j in range(dimension):
            sample[i][j] = float(i + j) / (size + dimension)
    print "external code(sample) = ", repr(external(sample))

except  :
    import sys
    print "t_NumericalMathFunction_exec_sample.py", sys.exc_type, sys.exc_value
