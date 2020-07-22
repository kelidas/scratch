
#This program repairs all EPS files (mainly boundary box) in folder and save them in new folder "correct_EPS".

import os
import platform

directory = "."
files = [v for v in os.listdir(directory) if os.path.splitext(v)[1]=='.pdf']

for i in range(0, len(files)):
    if platform.system() == 'Linux':
        fname = files[i][0:len(files[i])-4]
        cmd = "pdftops -eps {} {}.eps".format(files[i], fname)
    elif platform.system() == 'Windows':
        fname = files[i][0:len(files[i])-4]
        cmd = "pdf2ps {} {}.eps".format(files[i], fname)
    os.system(cmd)
    print(cmd)
    
