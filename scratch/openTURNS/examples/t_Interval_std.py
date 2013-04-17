#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

try :
    # The 1D interface
    interval1D = Interval(-3, 5)
    print "interval1D=", interval1D
    # The default interface
    size = 2
    defaultInterval = Interval(2)
    print "defaultInterval=", defaultInterval
    # Construction from 2 NumericalPoint
    p1 = NumericalPoint(2, -1.0)
    p2 = NumericalPoint(2, 2.0)
    print "interval from 2 points=", Interval(p1, p2)
    # Construction from 2 points and 2 flags
    flag1 = BoolCollection(2, False)
    flag2 = BoolCollection(2, True)
    interval = Interval(p1, p2, flag1, flag2)
    print "interval from 2 points and 2 flags=", interval
    # Accessors
    print "lower bound=", repr(interval.getLowerBound())
    print "upper bound=", repr(interval.getUpperBound())
    print "lower bound flags=", interval.getFiniteLowerBound()
    print "upper bound flags=", interval.getFiniteUpperBound()
    # Check if a given interval is empty
    print "interval [p1, p2] empty? ", Interval(p1, p2).isEmpty()
    print "interval [p2, p1] empty? ", Interval(p2, p1).isEmpty()
    # Intersection
    interval1 = Interval(p1, p2)
    p3 = NumericalPoint(2)
    p3[0]=0.5
    p3[1]=-1.5
    p4 = NumericalPoint(2)
    p4[0]=1.5
    p4[1]=2.5
    interval2 = Interval(p3, p4)
    print "intersection of ", interval1, " and ", interval2, " equals ", interval1.intersect(interval2)
except :
  import sys
  print "t_Interval_std.py", sys.exc_type, sys.exc_value

