'''
Created on Nov 6, 2014

@author: rhf

Calculate pi = 3.14159265 with Monte carlo simulation

Area(circle) / Area(square) = (pi*r^2)/(2*r)^2 = pi / 4

Based on:
http://web.chem.ucsb.edu/~kalju/MonteCarlo_1.html

'''

import numpy as np
import sys

def main():
    niter = 100000
    inTheSquare = 0
    for i in range(niter):
        x = 2 * (np.random.rand() - 0.5)
        y = 2 * (np.random.rand() - 0.5)
        z = x*x + y*y;
        if z <= 1:
            inTheSquare+=1
    pi = 4.0 * inTheSquare / niter
    print "# of trials = %d, inTheSquare = %.1f %% , estimate of pi = %.4f"%(niter,inTheSquare/float(niter)*100,pi)

if __name__ == '__main__':
    main()