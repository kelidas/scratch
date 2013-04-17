 
# -*- coding: cp1250 -*-
import  math
import operator
import string
import random
from numpy import matrix
from numpy import linalg

outfile = open('du2.txt', 'w')
outfile.write("%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n" % ("N", "l1", "l2", "l3", "q", "F1", "F2", "wb", "wc","--","M4","M5","X1","X2"))
outfile.write("==============================================================================================================\n")


n = 1

while n != 100:
    q = random.randrange(1,6,1)
    #print q 
    f1 = random.randrange(5,15,1)
    #print f1
    f2 = random.randrange(5,15,1)
    #print f2
    #f3 = random.randrange(10,100,5)*100
    #print f3
    x1 = 0
    x2 = x1 + float(random.randrange(4,9,2))
    x3 = x2 + float(random.randrange(1,5,1))
    x4 = x3 + float(random.randrange(1,5,1))
    #x3 = float(random.randrange(10,31,5))/10 + x2
    #y1 = 0
    #y2 = 4.
    #y2 = float(random.randrange(20,51,5))/10
    #x1 = 0.
    #x2 = 2.
    #x3 = 5.
    #y1 = 0.
    #y2 = 4.
    #l1 = abs(y1-y2)
    l1 = abs(x1-x2)
    l2 = abs(x2-x3)
    l3 = abs(x3-x4)
    wb = float(random.randrange(0,11,2))*0.1
    wc =float(random.randrange(0,11,2))*0.1
    print l1, ", ", l2, ", ", l3, ", ", q, ", ", f1, ", ", f2,", ", wb,", ", wc, "\n"
    #l3 = math.sqrt(l1**2+l3**2)
    #print l1,"\t", l2,"\t", l3
    #q=5000
    #f1=500
    #f2=17000
    #f3=4500
    #########vetknuti - konzola ##########
    #if ((v < 0 and rax >0) and (ma < 0 and(ma+am1) >0 and (ma+am1+am2) < 0) and (v < 0 and raxp > 0) and ((amp1)>0 and (amp1+amp2) < 0)):
    outfile.write("%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n" % (n, l1, l2, l3, q, f1, f2, wb,wc, "-----","-----","-----","-----","-----"))
        #outfile.write("%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s%-10s\n" % (n, l2, q, f1, f2, f3, 0, 0 + amp1,0 + amp1 +amp2,amp3,amp4,amp5))
        #print q, "\t", f1, "\t", f2,  "\t", f3
        #print l1,"\t", l2,"\t", l3, "\t", l4
        #print ma, "\t", ma + am1, "\t", ma + am1 +am2, "\t", am3, "\t", am4, "\t", am5
        #print 0, "\t", 0+amp1,"\t", 0+amp1+amp2
        #print "splneno"
        #print vysl
    n = n + 1
    #else:
        #print "nesplneno pro konzolu"
    

outfile.close()  
