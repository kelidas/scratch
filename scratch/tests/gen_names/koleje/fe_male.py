#!/usr/bin/python
# -*- coding: utf-8 -*-

block = 3
infile = open('names_C0%d.txt'%block, 'r')

lines = infile.readlines()
fem = 0
n_lin = 0
for line in lines:
    if line != '\n':
	n_lin += 1
	if line.endswith('ov\xe1\n'):
	    fem += 1
	else:
	    continue


print 'number of fem = %d of %d (%f)' % (fem, n_lin,fem/float(n_lin)*100)