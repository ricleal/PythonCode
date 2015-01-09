#!/usr/bin/env python

"""
First run:

python setup.py build_ext --inplace

Then:

python fib_run.py

"""

import demo
import numpy as np
import time
import threading

TIC = None
 
def tic():
    global TIC
    TIC = time.time()

def toc():
    """
    Return time in seconds
    """
    now = time.time()
    delta = now-TIC
    return delta

def main():
    
    # Test numpy
    m1 = 1 * np.random.random((50,50)).astype(np.float64)
    m2 = demo.getDummyMatrix(m1);
    print "m1:", m1
    print "m2:", m2
    
    tic()
    m3 = demo.matMult1(m1,m2)
    print toc()
    print "m3:", m3
    
    tic()
    m4 = np.zeros( (m1.shape[0], m2.shape[1]), dtype=np.float64)
    demo.matMult2(m1,m2,m4)
    print toc()
    print "m4:", m4
    
    
    A = np.random.random((1000, 1000))
    B = np.random.random((1000, 1000))
    C = np.zeros((A.shape[0], B.shape[1]))
    N = len (A)
    tic()
    t1 = threading.Thread( target = demo.matMult_part, args =(0, N//2, A, B, C))
    t2 = threading.Thread( target = demo.matMult_part, args =(N//2, N, A, B, C))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print "Parallel finished:", toc()

if __name__ == "__main__":
    print "Main started..."
    main()
    print "Main ended!"
