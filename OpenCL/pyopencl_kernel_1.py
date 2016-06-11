#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import pyopencl as cl
import pyopencl.array
from pyopencl.elementwise import ElementwiseKernel
from pyopencl.reduction import ReductionKernel

n = 10
a_np = np.ones(n).astype(np.float32)*2
b_np = np.ones(n).astype(np.float32)*2

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

a_g = cl.array.to_device(queue, a_np)
b_g = cl.array.to_device(queue, b_np)
res_g = cl.array.empty_like(a_g)

elem_wise_krnl = ElementwiseKernel(ctx,
    "float *a_g, float *b_g, float *res_g",
    "res_g[i] = a_g[i] * b_g[i]",
    "lin_comb"
)
elem_wise_event = elem_wise_krnl(a_g, b_g, res_g)

# np.set_printoptions(precision=2)
# print(res_g.get())

reduction_krnl = ReductionKernel(ctx, np.float32, neutral="0",
        reduce_expr="a+b", map_expr="x[i]",
        arguments="__global float *x")
res_reduction = reduction_krnl(res_g, queue=queue, wait_for=[elem_wise_event])

print(res_reduction.get())
