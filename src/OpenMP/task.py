
"""
DOES NOT WORK!

Traceback (most recent call last):
  File "task.py", line 15, in <module>
    lib = ct.cdll.LoadLibrary(os.path.join(p, 'libtask.so'))
  File "/usr/lib/python2.7/ctypes/__init__.py", line 443, in LoadLibrary
    return self._dlltype(name)
  File "/usr/lib/python2.7/ctypes/__init__.py", line 365, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: /home/rhf/git/PythonCode/src/OpenMP/libtask.so: undefined symbol: omp_get_thread_num

"""

import ctypes as ct
import numpy as np
from numpy.ctypeslib import as_ctypes

import os
import sys

p = os.path.dirname(os.path.realpath(__file__))

lib = ct.cdll.LoadLibrary(os.path.join(p, 'libtask.so'))
                        
# lib = ct.CDLL('libtask.so')

def set_N_threads(nthreads):
    lib.omp_set_num_threads(nthreads)
    
def do_some_task():
    SIZE = 1024
    
    input_array = 1 * np.random.random(SIZE).astype(np.float32)
    output_array = np.empty_like(input_array)
    
    lib.do_some_omp_task(as_ctypes(input_array),
                         as_ctypes(output_array),
                         ct.c_size_t(input_array.size))
    return output_array



if __name__ == "__main__":
    set_N_threads(8)
    out = do_some_task()
    print out.shape
