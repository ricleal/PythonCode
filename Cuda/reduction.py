from __future__ import print_function
from __future__ import absolute_import
import pycuda.driver as drv
import pycuda.tools
import pycuda.autoinit
import numpy as np
import numpy.linalg as la
from pycuda.compiler import SourceModule


mod = SourceModule("""
#include <stdio.h>
#include <stdlib.h>
#include <cuda.h>

__inline__ __device__
int warpReduceSum(int val) {
  for (int offset = warpSize/2; offset > 0; offset /= 2) 
    // val += __shfl_down(val, offset);
    val += __shfl_down_sync(0xFFFFFFFF, val, offset);
  return val;
}

__inline__ __device__
int blockReduceSum(int val) {

  static __shared__ int shared[32]; // Shared mem for 32 partial sums
  int lane = threadIdx.x % warpSize;
  int wid = threadIdx.x / warpSize;

  val = warpReduceSum(val);     // Each warp performs partial reduction

  if (lane==0) shared[wid]=val; // Write reduced value to shared memory

  __syncthreads();              // Wait for all partial reductions

  //read from shared memory only if that warp existed
  val = (threadIdx.x < blockDim.x / warpSize) ? shared[lane] : 0;

  if (wid==0) val = warpReduceSum(val); //Final reduce within first warp

  return val;
}

__global__ void deviceReduceKernel(int *in, int* out) {
  int sum = 0;
  int N = blockDim.x * gridDim.x;

  //printf(" %d", blockIdx.x * blockDim.x + threadIdx.x);

  //reduce multiple elements per thread
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; 
       i < N; 
       i += blockDim.x * gridDim.x) {
    sum += in[i];
  }
  sum = blockReduceSum(sum);
  if (threadIdx.x==0)
    out[blockIdx.x]=sum;
}

""")


N = 64*64
a = np.arange(N).astype(np.f32)

threads = 512 # Threads per block
blocks =  int(N / threads) # Number of blocks in the grid

print("Threads = {} Blocks = {}; Total = {}".format(threads, blocks, N))
# NP
reduction_np = np.sum(a)
print(reduction_np)

# GPU
dest = np.zeros(5)
device_reduce_kernel = mod.get_function("deviceReduceKernel")
device_reduce_kernel(
    drv.In(a),
    drv.Out(dest),
    block=(threads, 1, 1),
    grid=(blocks, 1),  # A grid is divided into blocks!
)

print(dest.astype(np.int32))
