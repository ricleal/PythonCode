from pyopencl import clrandom
import numpy as np
import pyopencl as cl

"""
Dot product element wise of 2 vector of 3d coordinates
Using Float3

"""

source = """
__kernel void gpu_mul(__global const float *a, __global const float *b, __global float *c) {

    int i = get_global_id(0);
    int j = get_global_id(1);

    int size_a = get_global_size(0);
    int size_b = get_global_size(1);

    float3 vec_a = vload3(i, a);
    float3 vec_b = vload3(j, b);

    int idx = i*size_b + j;
    //c[idx] = size_a + size_b;

    float res = dot(vec_a, vec_b);
    c[idx] = res;

} // execute over n "work items"
"""

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# create some data array to give as input to Kernel and get output
SIZE = 4
a_np = np.arange(SIZE*3).reshape(SIZE,3).astype(np.float32)
b_np = np.arange(SIZE*3, SIZE*3+SIZE*3).reshape(SIZE,3).astype(np.float32)
c_np = np.zeros((SIZE*SIZE)).astype(np.float32)

# create the buffers to hold the values of the input
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=a_np)
b_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=b_np)
# create output buffer
c_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, c_np.nbytes)

#Compilation
prg = cl.Program(ctx, source).build()

# Kernel is now launched
launch = prg.gpu_mul(queue, (SIZE,SIZE), None, a_buf, b_buf, c_buf)
# wait till the process completes
launch.wait()

cl.enqueue_read_buffer(queue, c_buf, c_np).wait()
# print the output
print "a:\n", a_np
print "b:\n", b_np
print "c:\n", c_np
