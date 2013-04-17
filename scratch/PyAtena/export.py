import subprocess
from multiprocessing import Pool
import os
import shutil


for i in range(2):
    
    infile = open('monitor_export.inp','r')
    infile_data = infile.read()
    infile.close()
    outfile = open('E:\Documents\python\workspace\AtenaScience\dogbone_rand\size_D\D_%02i/monitor_export.inp'%(i+1),'w')
    last = os.listdir('D_%02i/results'%(i+1))[-1]
    outfile.write('RESTORE "results\%s"\n'%(last))
    outfile.write(infile_data)
    outfile.close()

m=[]
for i in range(2):
    DIR = 'E:\Documents\python\workspace\AtenaScience\dogbone_rand\size_D\D_%02i' % (i+1)
    subprocess.call('AtenaConsole64.exe /D "%s" /extend_real_output_width /execute "%s"'%(DIR,'monitor_export.inp'))


print 'END!'
