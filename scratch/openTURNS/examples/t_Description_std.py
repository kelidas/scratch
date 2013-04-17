#! /usr/bin/env python.exe

from openturns import *

TESTPREAMBLE()

#Default constructor
desc1 = Description()
ref_desc1 = desc1

#Check method add()
desc1.add("X")
desc1.add("Y")

size = desc1.getSize()
print "size of desc1 = ", size

val1 = ref_desc1[0]
val2 = ref_desc1[1]

print "desc1[0] = ", val1
print "desc1[1] = ", val2

#Constructor with size */
desc2 = Description(2)
ref_desc2 = desc2

#Check operator[] methods 
desc2[0] = "a"
desc2[1] = "b"

val1 = ref_desc2[0]
val2 = ref_desc2[1]
print "desc2[0] = ", val1
print "desc2[1] = ", val2

#Copy constructor
desc3 = desc1
ref_desc3 = desc3

val1 = ref_desc3[0]
val2 = ref_desc3[1]
print "desc3[0] = ", val1
print "desc3[1] = ", val2

#Stream operator 
print "desc1 = ", ref_desc1

#Construction from sequence
desc4 = Description( ("A","B","C") )
print "desc4 = ", desc4

l = ["U", "I", "O", "P"]
desc5 = Description( l )
print "desc5 = ", desc5

sz = len(desc5)
i=0
for x in desc5:
    print "desc5[%01d,%01d] = %s" % (i,sz,x)
    i+=1
