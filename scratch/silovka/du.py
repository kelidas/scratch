 
# -*- coding: cp1250 -*-
import  math
import operator
import string
import random
from numpy import matrix
from numpy import linalg

outfile = open('du.txt', 'w')
outfile.write("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n" % ("N", "l2", "I1","I2", "I3", "q", "F1", "F2", "F3", "Ma", "M1", "M2","M3","M4","M5","X1","X2"))
outfile.write("==============================================================================================================\n")


n = 1

while n != 200:
    q = random.randrange(10,100,5)*100
    #print q 
    f1 = random.randrange(1,100,5)*100
    #print f1
    f2 = random.randrange(10,100,5)*200
    #print f2
    f3 = random.randrange(10,100,5)*100
    #print f3
    x1 = 0
    x2 = float(random.randrange(20,44,5))/10
    x3= x2 + 3.
    #x3 = float(random.randrange(10,31,5))/10 + x2
    y1 = 0
    y2 = 4.
    #y2 = float(random.randrange(20,51,5))/10
    #x1 = 0.
    #x2 = 2.
    #x3 = 5.
    #y1 = 0.
    #y2 = 4.
    l1 = abs(y1-y2)
    l2 = abs(x1-x2)
    l3 = abs(x2-x3)
    l4 = math.sqrt(l1**2+l3**2)
    #print l1,"\t", l2,"\t", l3
    #q=5000
    #f1=500
    #f2=17000
    #f3=4500
    #########vetknuti - konzola ##########
    rax = -(- l1 * q + f2)
    raz = f1 + f3
    ma = -(q * l1**2 / 2 + f1 * l2 / 2 - f2 * l1 + f3 * (l2 + l3 / 2))
    v = rax - l1 * q
    lm = l1/abs(v-rax) * rax
    am1 =rax *lm/2
    am2 = v * (l1- lm) /2
    am3 = ma + am1 + am2 + raz * l2/2
    am4 = am3 + (raz - f1) * l2/2
    am5 = am4 + l3/l4*f3 * l4 / 2
    #print ma, "\t", ma+am1,"\t", ma+am1+am2
    #
    m11 = l2 + l3
    m12 = l2 + l3
    m13 = l2 + l3
    m14 = m13 - l2/2
    m15 = m13 - l2
    m16= m15 -l3/2
    m17 = m15 -l3
    m21 = 0
    m22 = - l1/2
    m23 = -l1
    m24= -l1
    m25 = -l1
    m26 = -l1/2
    m27 = 0
    m=1./8.*q*l1*l1/1000.
    E1 = 20.e9
    I1 = float(random.randrange(1,5,1))*0.00001
    E2 = 20.e9
    I2 = float(random.randrange(1,5,1))*0.00001
    E3 = 20.e9
    I3 = float(random.randrange(1,5,1))*0.00001
    #prut 1
    a111= 1./(E1*I1)*m11 * m11 * l1
    a122 = 1./(E1*I1)*1./3. * m23 *m23 *l1
    a112 = 1./(E1*I1)*1./2.*m11*m23*l1
    a120 = 1./(E1*I1)*(1./2000.*ma*m23*l1-1./3.*(abs((ma+am1+am2)/1000)+ma/1000.)*m23*l1+1./3.*m*m23*l1)
    a110 = 1./(E1*I1)*(m11*ma/1000.*l1 + 2./3.*m*m11*l1 - 1./2.*m11*(abs((ma+am1+am2)/1000.)+ma/1000.)*l1)
    #prut 2
    a211= 1./(E2*I2)*(1./6.*(m13*(m13*2+m15)+m15*(m13+2*m15))*l2)
    a222 = 1./(E2*I2)*m23*m23*l2
    a212 = 1./(E2*I2)*1./2.*(m13+m15)*m23*l2
    a220 = 1./(E2*I2)*(1./2000. *(2*am3-am4+am4)*m23*l2 + 1./2000.*m23*(ma+am1+am2-(2*am3-am4))*l2/2)
    a210 = 1./(E2*I2)*(1./6.*((2*am3-am4)/1000*(m13*2+m15)+am4/1000*(m13+2*m15))*l2+(ma+am1+am2-(2*am3-am4))/6000.*l2/2./l2*(m13*(3*l2-l2/2)+m15*l2/2))
    #prut 3
    a311 = 1./(E3*I3)*1./3.*m15*m15*l4
    a322 = 1./(E3*I3)*1./3.*m25*m25*l4
    a321 = 1./(E3*I3)*1./3.*m25*m15*l4
    a320 = 1./(E3*I3)*(1./6. *m25*am4/1000.*l4/2/l4*(3*l4-l4/2))
    a310 = 1./(E3*I3)*(1./6. *m15*am4/1000.*l4/2/l4*(3*l4-l4/2))
    a11 = a111+a211+a311
    a22 = a122+a222+a322
    a12 = a112+a212+a321
    a10 = a110+a210+a310
    a20 = a120+a220+a320
    matice = [[a11,a12],[a12,a22]]
    vektor = [[a10],[a20]]
    matA=matrix(linalg.inv(matice))
    vect=matrix(vektor)
    vysl = matA*vect
    ###############prosty nosnik ###########
    raxp = -(- l1 * q + f2)
    rbzp = (f3 * (l1 + l3/2) -f1 *l2/2 - f2 * l1)/(l1+l3)
    razp = -rbzp +f3 +f1
    amp1 = raxp *lm/2
    amp2 = v * (l1- lm) /2
    amp3 = 0 + amp1 + amp2 + raz * l2/2
    amp4 = amp3 + (raz - f1) * l2/2
    amp5 = amp4 + l3/l4*f3 * l4 / 2
    #print 0, "\t", 0+am2,"\t", 0+am2+amm2
    if ((v < 0 and rax >0) and (ma != 0 and(ma+am1) >0 and (ma+am1+am2) < 0) and (v < 0 and raxp > 0) and ((amp1)>0 and (amp1+amp2) < 0)):
        outfile.write("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n" % (n, l2, I1, I2, I3, q, f1, f2, f3, ma, ma + am1,ma + am1 +am2,am3,am4,am5,float(vysl[0]*1000),float(vysl[1]*1000)))
        #outfile.write("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n" % (n, l2, q, f1, f2, f3, 0, 0 + amp1,0 + amp1 +amp2,amp3,amp4,amp5))
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
