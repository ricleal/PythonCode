import multiprocessing
import ctypes
import numpy as np
import os
import time
import random

'''
Non Shared array!


With numpy this does not work!!!

The function my_func does not change the array!

$ python3 non_shared_array.py 
[[0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]]

Unique values: [0.]

'''

shared_array = np.zeros((10,10))


# Parallel processing
def my_func(i, array=shared_array):
    '''
    For every row i assigns the pid of the process
    '''
    array[i,:] = os.getpid()
    time.sleep(random.uniform(0, 0.5))

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    pool.map(my_func, range(10))

print(shared_array)
print("\nUnique values:", np.unique(shared_array))
