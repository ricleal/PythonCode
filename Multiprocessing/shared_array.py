import os
import time
import random
import multiprocessing
import ctypes
import numpy as np


'''
Shared array!
'''

shared_array_base = multiprocessing.Array(ctypes.c_double, 10*10)
shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
shared_array = shared_array.reshape(10, 10)


# Parallel processing
def my_func(i, array=shared_array):
    array[i,:] = os.getpid()
    time.sleep(random.uniform(0, 0.5))

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    pool.map(my_func, range(10))

print(shared_array)
print("\nUnique values:", np.unique(shared_array))
