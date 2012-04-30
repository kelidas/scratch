'''
Created on Apr 10, 2012

@author: kelidas
'''

# test masked array efficiency
import numpy as np
import platform

if platform.system() == 'Linux':
    from time import time as sysclock
elif platform.system() == 'Windows':
    from time import clock as sysclock

def main():

    a = np.linspace(0, 1, 50000)
    b = np.linspace(0, 1, 50000)
    a[a > 0.5] = 0
    b[b > 0.5] = 0
    a_m = np.ma.array(a, mask=a > 0.5)
    b_m = np.ma.array(b, mask=b > 0.5)


    start = sysclock()
    res1 = a * b
    print sysclock() - start, 'full array'

    start = sysclock()
    res2 = a_m * b_m
    print sysclock() - start, 'numpy masked array'

    res3 = a
    start = sysclock()
    res3[res3 > 0] *= b[res3 > 0]
    print sysclock() - start, 'mask'

    print 'arrays are equal', np.array_equal(res1, res2) and np.array_equal(res2, res3)

if __name__ == '__main__':
    main()






