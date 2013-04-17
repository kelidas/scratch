import matplotlib.pyplot as p
from os.path import join
import numpy as np


for i in range(2):
    DIR = "D_%02i\exports"%(i+1)

    x = np.genfromtxt(join(DIR,'displacement.txt'), skip_header=13, skip_footer=9)
    y = np.genfromtxt(join(DIR,'reaction.txt'), skip_header=13, skip_footer=9)


    p.plot(x[:,1],y[:,1])
p.show()
