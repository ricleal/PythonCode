#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pyopencl as cl
import pyopencl.array
import time
from pyopencl.elementwise import ElementwiseKernel
from pyopencl.reduction import ReductionKernel

'''
Run as:
PYOPENCL_CTX='0:2' PYOPENCL_COMPILER_OUTPUT=1 python pyopencl_kernel_1.py

Bit wise operation on Vector of 4d coordinates (4th is zero)
followed by a Reduction
Does not work on macos....

'''
# float4 is better than float3! Append 0 as w
n = 10000000 * 3

z = np.zeros((n,1), dtype=np.float32)
a_np = np.append(np.random.random((n,3)).astype(np.float32), z, axis=1)
b_np = np.append(np.random.random((n,3)).astype(np.float32), z, axis=1)


ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

a_g = cl.array.to_device(queue, a_np)
b_g = cl.array.to_device(queue, b_np)

res_g = cl.array.empty(queue, shape=(n,), dtype=np.float32)

start = time.time()

elem_wise_krnl = ElementwiseKernel(ctx,
    arguments="float4 *a_g, float4 *b_g, float *res_g",
    operation="res_g[i] = dot(a_g[i],b_g[i])",
    name="elem_wise_krnl"
)
elem_wise_event = elem_wise_krnl(a_g, b_g, res_g)

elem_wise_time = time.time()

# np.set_printoptions(precision=2)
# print(res_g.get())
# print(res_g.get().shape)
# print(res_g.get()[:10])

reduction_krnl = ReductionKernel(ctx,
    dtype_out=np.float32,
    neutral="0",
    reduce_expr="a+b",
    map_expr="x[i]",
    arguments="__global float *x",
    name="reduction_krnl",
)

res_reduction = reduction_krnl(res_g, queue=queue, wait_for=[elem_wise_event])

reduction_time = time.time()

print("elem_wise_time: {}".format(elem_wise_time-start))
print("reduction_time: {}".format(reduction_time-elem_wise_time))
print("Total: {}".format(reduction_time-start))
#print(res_reduction)

print(res_reduction.get())
