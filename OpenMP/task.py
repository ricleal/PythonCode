import ctypes as ct
import numpy as np
from numpy.ctypeslib import as_ctypes

import os
import sys

p = os.path.dirname(os.path.realpath(__file__))

lib = ct.cdll.LoadLibrary(os.path.join(p, 'libtask.so'))

def set_N_threads(nthreads):
    lib.omp_set_num_threads(nthreads)


def do_some_task():
    SIZE = 100

    input_array = 100 * np.random.random(SIZE)
    print("Input Max={} Min={} Shape={}".format(
        input_array.max(), input_array.min(), input_array.shape))
    input_array = np.round(input_array).astype(np.int64)
    print("Input Max={} Min={} Shape={}".format(
        input_array.max(), input_array.min(), input_array.shape))
    output_array = np.empty_like(input_array)

    print("Starting openmp part...")
    lib.do_some_omp_task(as_ctypes(input_array),
                         as_ctypes(output_array),
                         ct.c_size_t(input_array.size))
    print("End!")
    return output_array


if __name__ == "__main__":
    set_N_threads(56)
    out = do_some_task()
    print("Out Max={} Min={} Shape={}".format(out.max(), out.min(), out.shape))
