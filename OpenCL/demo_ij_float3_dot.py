from pyopencl import clrandom
import numpy as np
import pyopencl as cl

"""
As others mentioned, float3 (and other type3 types) behave as float4 (and other type4 types) for the purposes of size and alignment. This could also be seen using the built-in vec_step function, which returns the number of elements in the input object's type, but returns 4 for type3 objects.

If your host code generates a packed float3 array - with each object taking the size and alignment of just 3 floats - then the proper way to use it from OpenCL is:

Use a float* parameter instead of float3*
Load the data using vload3
Store data using vstore3

Vector 3 is slow!!!!
http://stackoverflow.com/questions/20200203/using-own-vector-type-in-opencl-seems-to-be-faster

"""

source = """
__kernel void gpu_mul(__global const float *a, __global const float *b, __global float *c) {

    int i = get_global_id(0); //iterates the vector
    int j = get_global_id(1);
    int k = get_global_id(2);

    int size_vector = get_global_size(0);
    int size_a = get_global_size(1);
    int size_b = get_global_size(2);


    int c_idx = i + j * size_vector + k * size_vector * size_a;
    int a_idx =  i + j*size_vector;
    int b_idx =  i + k*size_vector;

    // sum element by element
    c[c_idx] = a[a_idx] + b[b_idx];


} // execute over n "work items"
"""

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# create some data array to give as input to Kernel and get output
SIZE = 4
a_np = np.arange(SIZE*3).reshape(SIZE,3).astype(np.float32)
b_np = np.arange(SIZE*3, SIZE*3+SIZE*3).reshape(SIZE,3).astype(np.float32)
c_np = np.zeros((SIZE*SIZE,3)).astype(np.float32)

# create the buffers to hold the values of the input
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=a_np)
b_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=b_np)
# create output buffer
c_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, c_np.nbytes)

#Compilation
prg = cl.Program(ctx, source).build()

# Kernel is now launched
launch = prg.gpu_mul(queue, (3,SIZE,SIZE), None, a_buf, b_buf, c_buf)
# wait till the process completes
launch.wait()

cl.enqueue_read_buffer(queue, c_buf, c_np).wait()
# print the output
print "a:\n", a_np
print "b:\n", b_np
print "c:\n", c_np
