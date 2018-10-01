#!/usr/bin/env python3
import multiprocessing
import os
import sys
import time
import ctypes
from multiprocessing import Pool

import numpy as np

'''

'''

# create a 1D array, size = 10*10, type double
shared_array_base = multiprocessing.Array(ctypes.c_double, 10*100*100)
# Make it shared
shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
# Make it 2D
shared_array = shared_array.reshape(10, 100, 100)

# let's put some random data in the datasets
for i in range(10):
    shared_array[i] = np.random.rand(100, 100)

normalization_dataset = np.ones_like(shared_array[i])-0.99


def normalize(i):
    '''
    For every row i assigns the pid of the process
    '''
    print("Child pid is: {}".format(os.getpid()))
    time.sleep(0.1)
    shared_array[i] /= normalization_dataset
    time.sleep(0.1)
    


if __name__ == '__main__':
    print("Parent pid is: {}".format(os.getpid()))
    pool = Pool(processes=10)
    print("Before normalization:\n", shared_array[1,1,:10])
    pool.map(normalize, range(10))
    print("After normalization:\n", shared_array[1,1,:10])