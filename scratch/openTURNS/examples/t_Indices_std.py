#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    size = 4
    indices = Indices(size, 0)
    for i in range(size):
	indices[i] = i
    print "indices=", indices
    print "are indices valid with bound=", size, "? ", indices.check(size)
    print "are indices valid with bound=", size / 2, "? ", indices.check(size / 2)
    indices[0] = indices[size-1]
    print "indices after transformation=", indices
    print "are indices valid with bound=", size, "? ", indices.check(size)
except :
  import sys
  print "t_Indices_std.py", sys.exc_type, sys.exc_value

