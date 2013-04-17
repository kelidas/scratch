import os
import re
import sys
import urllib



for block in range(3):
    infile = open('names_C0%d.txt'%(block+1),'w')
    for floor in range(7):
        for room in range(32):
            f = urllib.urlopen("http://www/search/index.html?str=c0%s-%s" % (block+1, str((floor+2)*100+room+1)))
            html = f.read()
            m = re.findall('</font> (\S+) (\S+)</th>',html)
            print 'C0%s-'%(block+1),(floor+2)*100+room+1, m, '\n'
            if len(m)!=0:
                for item in m:
                    infile.write('C0%s-%s\t%s %s\n'%( str(block+1),str((floor+2)*100+room+1),item[0],item[1]))
		infile.write('\n')
            f.close()
    infile.close()
