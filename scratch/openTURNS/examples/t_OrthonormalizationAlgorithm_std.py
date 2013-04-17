#! /usr/bin/env python.exe

from openturns import *
from math import *

TESTPREAMBLE()

try :
    distribution = Triangular(-1.0, 0.3, 1.0)
    algo = OrthonormalizationAlgorithm(Distribution(distribution))
    print "algo=", algo
    print "measure=", algo.getMeasure()
    algo.setMeasure(Distribution(Triangular(-1.0, -0.2, 1.0)))
    print "new measure=", algo.getMeasure()
      
except :
    import sys
    print "t_OrthonormalizationAlgorithm_std.py", sys.exc_type, sys.exc_value

