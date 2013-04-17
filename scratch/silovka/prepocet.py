# -*- coding: cp1250 -*-

import  math
import operator
import string
import random
from numpy import matrix
from numpy import linalg
import numpy

def vynechRadky(n):
    n = 10  #pocet vynechanych radku
    for i in range(0, n - 1):
        infile.readline()

def nactiData():
    pocet = len(nazvySouboru())                          
    text = pocet * ['']
    soubor = pocet * [""]
    soubor = nazvySouboru()
    mnoz = 0
    for i in range(0,pocet):
        infile = open(soubor[i],'r')
        for j in infile.readlines():
            mnoz+=1
        infile.close()
    seznam = [''] * (mnoz)
    mnoz = 0
    for i in range(0,pocet):
        infile = open(soubor[i],'r')
        for j in infile.readlines():
            seznam[mnoz] =  j.split() 
            mnoz+=1
        infile.close()     
    #print mnoz 
    #print seznam     
    #for i in range(0, mnoz-1):
        #for j in range(0, len(seznam[i])):
            #print seznam[i][j],'\t'
        #print '\n'

def readTitleLines(f):
    '''Read and echo two title lines'''
    t1 = f.readline()
    t2 = f.readline().replace('\n','')
    #print t1,t2

def readLineOfNumbers(f):
    s = f.readline()
    #print s.replace('\n','')
    ls = s.split()
    return [float(v) for v in ls]

#konec = 'a'
#while konec!='k':
infile = open('prepocet.txt', 'r')

numrow = 0
for j in infile.readlines():
    numrow+=1
#print numrow
infile.close()
infile = open('prepocet.txt', 'r')

data = [''] * numrow

readTitleLines(infile)
for i in range(0, numrow-2):
    data[i] = readLineOfNumbers(infile)

#x1 = 0
#x2 = float(random.randrange(20,44,5))/10
#x3= x2 + 3.
#x3 = float(random.randrange(10,31,5))/10 + x2
#y1 = 0
#y2 = 4.
#y2 = float(random.randrange(20,51,5))/10
#x1 = 0.
#x2 = 2.
#x3 = 5.
#y1 = 0.
#y2 = 4.
l1 = 4.
#l2 = abs(x1-x2)
l3 = 3.
l4 = math.sqrt(l1**2+l3**2)
E1 = 20.e9
#I1 = float(random.randrange(1,5,1))*0.00001
E2 = 20.e9
#I2 = float(random.randrange(1,5,1))*0.00001
E3 = 20.e9
#I3 = float(random.randrange(1,5,1))*0.00001
outfile = open('du_prepocet.txt', 'w')
outfile.write("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n" % ("N", "l2", "I1","I2", "I3", "q", "F1", "F2", "F3", "Ma", "M1", "M2","M3","M4","M5","X1","X2"))
outfile.write("==============================================================================================================\n")


#print "EI je konst. [aa][nn]"
#dat=raw_input("EI je konst. [a][n]: ")
#print "zadej n: "
#pocn=int(input())
dat="n"
for i in range(0,numrow-2):#(0,numrow-2)(0, pocn)
    n=data[i][0]
    l2=data[i][1]
    I1=data[i][2]
    I2=data[i][3]
    I3=data[i][4]
    q=data[i][5]
    f1=data[i][6]
    f2=data[i][7]
    f3=data[i][8]
        #########vetknuti - konzola ##########
    rax = -(- l1 * q + f2)
    raz = f1 + f3
    ma = -(q * l1**2 / 2. + f1 * l2 / 2. - f2 * l1 + f3 * (l2 + l3 / 2.))
    v = rax - l1 * q
    lm = l1/abs(v-rax) * rax
    am1 =rax *lm/2
    am2 = v * (l1- lm) /2.
    am3 = ma + am1 + am2 + raz * l2/2.
    am4 = am3 + (raz - f1) * l2/2.
    am5 = am4 + l3/l4*f3 * l4 / 2.
    #print ma, "\t", ma+am1,"\t", ma+am1+am2
    #
    m11 = l2 + l3
    m12 = l2 + l3
    m13 = l2 + l3
    m14 = m13 - l2/2.
    m15 = m13 - l2
    m16= m15 -l3/2.
    m17 = m15 -l3
    m21 = 0
    m22 = - l1/2.
    m23 = -l1
    m24= -l1
    m25 = -l1
    m26 = -l1/2.
    m27 = 0
    m=1./8.*q*l1*l1/1000.
    if dat == 'a':
        E1 = 1
        I1 = 1
        E2 = 1
        I2 = 1
        E3 = 1
        I3 = 1
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
    a320 = 1./(E3*I3)*(1./6. *m25*am4/1000.*l4/2./l4*(3.*l4-l4/2.))
    a310 = 1./(E3*I3)*(1./6. *m15*am4/1000.*l4/2./l4*(3.*l4-l4/2.))
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
    rbzp = -(-q*(l1*l1/2.)-f1 * l2/2. + f2*l1 - f3*(l2+l3/2.))/(l2+l3)
    razp = -rbzp +f3 +f1
    mpa=0
    amp1 = raxp *lm/2.
    amp2 = raxp*l1 - q*(l1*l1/2.)
    amp3 = amp2 + razp * l2/2.
    amp4 = amp3 + (razp-f1)*l2/2.
    amp5 = rbzp*l3/2.
    #
    mp11 = float(l2 + l3)/float(l2+l3)
    mp12 = float(l2 + l3)/float(l2+l3)
    mp13 = float(l2 + l3)/float(l2+l3)
    mp14 = mp13-float(l2/2.)/float(l2+l3)
    mp15 = mp13 - float(l2)/float(l2+l3)
    mp16= mp15 -float(l3/2.)/float(l2+l3)
    mp17 = mp15 -float(l3)/float(l2+l3)
    mp21 = 0
    mp22 = (- l1/2.)
    mp23 = (-l1)
    mp24= (-l1)
    mp25 = (-l1)
    mp26 = (-l1/2.)
    mp27 = 0
    mp=1./8.*q*l1*l1/1000.
    #prut 1
    ap111= 1./(E1*I1)*mp11 * mp11 * l1
    ap122 = 1./(E1*I1)*1./3. * mp23 *mp23 *l1
    ap112 = 1./(E1*I1)*1./2.*mp11*mp23*l1
    ap120 = 1./(E1*I1)*(1./3.*amp2/1000.*mp23*l1 + 1./3.*l1*mp*mp23)
    ap110 = 1./(E1*I1)*(amp2/1000.*l1*mp11/2. + 2./3.*l1*mp*mp11)
    #prut 2
    ap211= 1./(E2*I2)*(1./6.*(mp13*(mp13*2+mp15)+mp15*(mp13+2*mp15))*l2)
    ap222 = 1./(E2*I2)*mp23*mp23*l2
    ap212 = 1./(E2*I2)*1./2.*(mp13+mp15)*mp23*l2
    ap220 = 1./(E2*I2)*((amp2/1000.+amp3/1000.)/4*l2+(amp3/1000.+amp4/1000.)/4*l2)*mp23
    ap210 = 1./(E2*I2)*((1./6.*((mp13*(2*(2*amp3/1000.-amp4/1000.)+amp4/1000.))+mp15*((2*amp3/1000.-amp4/1000.)+2*amp4/1000.))*l2)+(-2.*amp3/1000.+amp4/1000.+amp2/1000.)/6. *l2/2./l2*(mp13*(3*l2-l2/2.)+mp15*l2/2.))
    #prut 3
    ap311 = 1./(E3*I3)*1./3.*mp15*mp15*l4
    ap322 = 1./(E3*I3)*1./3.*mp25*mp25*l4
    ap321 = 1./(E3*I3)*1./3.*mp25*mp15*l4
    ap320 = 1./(E3*I3)*((1./3.*l4*2.*amp5/1000.*mp25)+(1./6.*(amp4-2*amp5)/1000.*mp25*1./2.*(3*l4-l4/2)))
    ap310 = 1./(E3*I3)*((1./3.*l4*2.*amp5/1000.*mp15)+(1./6.*(amp4-2*amp5)/1000.*mp15*1./2.*(3*l4-l4/2)))
    ap11 = ap111+ap211+ap311
    ap22 = ap122+ap222+ap322
    ap12 = ap112+ap212+ap321
    ap10 = ap110+ap210+ap310
    ap20 = ap120+ap220+ap320
    #
    maticep = [[ap11,ap12],[ap12,ap22]]
    vektorp = [[ap10],[ap20]]
    matpA=matrix(linalg.inv(maticep))
    vectp=matrix(vektorp)
    vyslp = matpA*vectp
    d=linalg.norm(maticep,ord=+numpy.inf)*linalg.norm(matpA,ord=+numpy.inf)
    print d


    #print 0, "\t", 0+am2,"\t", 0+am2+amm2
    #if ((v < 0 and rax >0) and (ma != 0 and(ma+am1) >0 and (ma+am1+am2) < 0) and (v < 0 and raxp > 0) and ((amp1)>0 and (amp1+amp2) < 0)):
    outfile.write("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n" % (n, l2, I1, I2, I3, q, f1, f2, f3, ma, ma + am1,ma + am1 +am2,am3,am4,am5,float(vysl[0]*1000),float(vysl[1]*1000),amp1,amp2,amp3,amp4,amp5))
        #outfile.write("%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n" % (n, l2, q, f1, f2, f3, 0, 0 + amp1,0 + amp1 +amp2,amp3,amp4,amp5))
        #print q, "\t", f1, "\t", f2,  "\t", f3
        #print l1,"\t", l2,"\t", l3, "\t", l4
        #print ma, "\t", ma + am1, "\t", ma + am1 +am2, "\t", am3, "\t", am4, "\t", am5
        #print 0, "\t", 0+amp1,"\t", 0+amp1+amp2
        #print "splneno"
        #print vysl
        #n = n + 1
    #else:
        #print "nesplneno pro konzolu"

print "n = ", n, "\n"\
    "l2 = ", l2, "\n"\
    "I1 = ", I1, "\n"\
    "I2 = ", I2, "\n"\
    "I3 = ", I3, "\n"\
    "q = ", q, "\n"\
    "f1 = ", f1, "\n"\
    "f2 = ", f2, "\n"\
    "f3 = ", f3, "\n"\
    "ma = ", ma, "\n"\
    "m1 = ", ma + am1, "\n"\
    "m2 = ", ma + am1 +am2, "\n"\
    "m3 = ", am3, "\n"\
        "m4 = ", am3, "\n"\
        "m5 = ", am4, "\n"\
        "m6 = ", am5, "\n"\
        "X1 svisle = ", float(vysl[0]*1000), "\n"\
        "X2 vodorovne = ", float(vysl[1]*1000), "\n"\
        "map = ", mpa, "\n"\
        "m1p = ", amp1, "\n"\
        "m2p = ", amp2, "\n"\
        "m3p = ", amp3, "\n"\
        "m4p = ", amp4, "\n"\
        "m5p = ", amp5, "\n"\
        "X1 = ", float(vyslp[0]*1000), "\n"\
        "X2 = ", float(vyslp[1]*1000)

print \
      "Jako konzola", "\n"\
"a111 = ", a111, "\n"\
"a122 = ", a122, "\n"\
"a112 = ", a112, "\n"\
"a120 = ", a120, "\n"\
"a110 = ", a110, "\n"\
"a211 = ", a211, "\n"\
"a222 = ", a222, "\n"\
"a212 = ", a212, "\n"\
"a220 = ", a220, "\n"\
"a210 = ", a210, "\n"\
"a311 = ", a311, "\n"\
"a322 = ", a322, "\n"\
"a321 = ", a321, "\n"\
"a320 = ", a320, "\n"\
"a310 = ", a310, "\n"\
"a11 = ",  a11, "\n"\
"a22 = ",  a22, "\n"\
"a12 = ",  a12, "\n"\
"a10 = ",  a10, "\n"\
"a20 = ",  a20, "\n"\
"Jako prostý nosník", "\n"\
"ap111 = ", ap111, "\n"\
"ap122 = ", ap122, "\n"\
"ap112 = ", ap112, "\n"\
"ap120 = ", ap120, "\n"\
"ap110 = ", ap110, "\n"\
"ap211 = ", ap211, "\n"\
"ap222 = ", ap222, "\n"\
"ap212 = ", ap212, "\n"\
"ap220 = ", ap220, "\n"\
"ap210 = ", ap210, "\n"\
"ap311 = ", ap311, "\n"\
"ap322 = ", ap322, "\n"\
"ap321 = ", ap321, "\n"\
"ap320 = ", ap320, "\n"\
"ap310 = ", ap310, "\n"\
"ap11 = ",  ap11, "\n"\
"ap22 = ",  ap22, "\n"\
"ap12 = ",  ap12, "\n"\
"ap10 = ",  ap10, "\n"\
"ap20 = ",  ap20


outfile.close()
#text = infile.read()
#infile.close()
#konec = raw_input('Pro konec zadej [k]: ')
#print "Konec!!!"
