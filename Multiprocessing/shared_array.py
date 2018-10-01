import os
import time
import random
import multiprocessing
import ctypes
import numpy as np


'''
Shared array!

You should get something similar to that.
Every invocation to the parallel function writes a row with its pid

$ python3 shared_array.py 
[[36559. 36559. 36559. 36559. 36559. 36559. 36559. 36559. 36559. 36559.]
 [36560. 36560. 36560. 36560. 36560. 36560. 36560. 36560. 36560. 36560.]
 [36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561.]
 [36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562.]
 [36559. 36559. 36559. 36559. 36559. 36559. 36559. 36559. 36559. 36559.]
 [36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562.]
 [36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561.]
 [36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562. 36562.]
 [36560. 36560. 36560. 36560. 36560. 36560. 36560. 36560. 36560. 36560.]
 [36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561. 36561.]]

Unique values: [36559. 36560. 36561. 36562.]

'''

# create a 1D array, size = 10*10, type double
shared_array_base = multiprocessing.Array(ctypes.c_double, 10*10)
# Make it shared
shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
# Make it 2D
shared_array = shared_array.reshape(10, 10)


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
