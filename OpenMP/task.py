import ctypes as ct
import numpy as np
from numpy.ctypeslib import as_ctypes
from timeit import default_timer as timer
import datetime
import os
import sys

p = os.path.dirname(os.path.realpath(__file__))

lib = ct.cdll.LoadLibrary(os.path.join(p, 'libtask.so'))

def set_N_threads(nthreads):
    lib.omp_set_num_threads(nthreads)


def do_some_task():
    SIZE = 1000
    np.random.seed(0)

    input_array = 100 * np.random.random(SIZE)
    input_array = np.round(input_array).astype(np.int64)
    output_array = np.empty_like(input_array)

    print("Starting openmp part...")
    start = timer()
    lib.do_some_omp_task(as_ctypes(input_array),
                         as_ctypes(output_array),
                         ct.c_size_t(input_array.size))
    end = timer()
    print("End... Elapsed time: {:0>8}".format(datetime.timedelta(seconds=(end - start))))
    return output_array


if __name__ == "__main__":
    set_N_threads(32)
    out = do_some_task()
    print("Out Max={} Min={} Shape={}".format(out.max(), out.min(), out.shape))
