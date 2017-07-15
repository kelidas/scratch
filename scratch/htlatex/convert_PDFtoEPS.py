
#This program repairs all EPS files (mainly boundary box) in folder and save them in new folder "correct_EPS".

import os
import platform

directory = "."
files = [v for v in os.listdir(directory) if os.path.splitext(v)[1]==".pdf"]

for i in range(0, len(files)):
    if platform.system() == 'Linux':
        os.system("pdftops -eps "+files[i]+" "+files[i][0:len(files[i])-4]+".eps")
        print "pdftops -eps "+files[i]+" "+files[i][0:len(files[i])-4]+".eps"
    elif platform.system() == 'Windows':
        os.system("pdf2ps "+files[i]+" "+"EPS\\"+files[i][0:len(files[i])-4]+".eps")
        print "pdf2ps "+files[i]+" "+files[i][0:len(files[i])-4]+".eps"
    
