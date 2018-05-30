from __future__ import print_function
from __future__ import absolute_import
import pycuda.driver as drv
import pycuda.tools
import pycuda.autoinit
import numpy as np
import numpy.linalg as la
from pycuda.compiler import SourceModule

N = 1024*1024
BLOCK_SIZE = 32

mod = SourceModule("""
__global__ void multiply_them(float *dest, float *a, float *b)
{
  int i = threadIdx.x + blockDim.x * blockIdx.x;
  dest[i] = a[i] * b[i];
}
""")

multiply_them = mod.get_function("multiply_them")

a = np.arange(N).astype(np.float32)
b = np.ones(N).astype(np.float32)

dest = np.zeros_like(a)
multiply_them(
    drv.Out(dest),
    drv.In(a), drv.In(b),
    block=(BLOCK_SIZE, 1, 1),
    grid=(N/BLOCK_SIZE, 1),  # A grid is divided into blocks!
)

print("N = {}".format(N))
print(dest.astype(np.int32))
