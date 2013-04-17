#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try:
    size = 10
    for dimension in range(1, 4):
	f = EnumerateFunction(dimension)
	print "First", size, " values for dimension", dimension
	for index in range(size):
	    print "index=", index, f(index)
except : 
    import sys
    print "t_EnumerateFunction_std.py", sys.exc_type, sys.exc_value

