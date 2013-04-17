#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :

    # Analytical construction
    input = Description(4)
    input[0] = "x0"
    input[1] = "x1"
    input[2] = "x2"
    input[3] = "x3"
    print  "input=" , input
    output = Description(2)
    output[0] = "y0"
    output[1] = "y1"
    print  "output=" , output
    formulas = Description(output.getSize())
    formulas[0] = "x0+sin(x1)+x2"
    formulas[1] = "2*x0+2*x1+2*x2"
    print  "formulas=" , formulas
    analytical = NumericalMathFunction(input, output, formulas)

    print  "analytical=" , analytical

    # Does it work?
    x = NumericalPoint(analytical.getInputDimension(), 1.0)
    print  "x=" , repr(x)
    print  "analytical(x)=" , repr(analytical(x))

except :
    import sys
    print "t_NumericalMathFunction_analytical.py", sys.exc_type, sys.exc_value
