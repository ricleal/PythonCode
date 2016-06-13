from pyopencl import clrandom
import numpy as np
import pyopencl as cl
import time

"""
Dot product element wise of 2 vector of 3d coordinates
Using Float3

"""

source = """
__kernel void elementwise(__global const float *a, __global const float *b, __global float *c) {

    int i = get_global_id(0);
    int j = get_global_id(1);

    // int size_a = get_global_size(0);
    int size_b = get_global_size(1);

    float3 vec_a = vload3(i, a);
    float3 vec_b = vload3(j, b);

    int idx = i*size_b + j;
    //c[idx] = size_a + size_b;

    float res = dot(vec_a, vec_b);
    c[idx] = res;

} // execute over n "work items"


__kernel void reduce(__global float *data,
    __local float* partial_sums,
    __global float* output)
{
    int lid = get_local_id(0);
    int group_size = get_local_size(0);

    float3 v = vload3(get_global_id(0), data);
    vstore3 (v,lid,partial_sums);
 	//partial_sums[lid] = data[get_global_id(0)];

    barrier(CLK_LOCAL_MEM_FENCE);

    for(int i = group_size/2; i>0; i >>= 1) {
        if(lid < i) {
            float3 v = vload3(lid + i, partial_sums);
            float3 va = vload3(lid, partial_sums);
            vstore3(v+va,lid,partial_sums);
            //partial_sums[lid] += partial_sums[lid + i];
        }
        barrier(CLK_LOCAL_MEM_FENCE);
    }

    if(lid == 0) {
        float3 v = vload3(0, partial_sums);
        vstore3(dot(v, (float3)(1.0f)),get_group_id(0),output);

        //output[get_group_id(0)] = dot(partial_sums[0], (float4)(1.0f));
    }
}

"""

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# create some data array to give as input to Kernel and get output
SIZE = 10000
a_np = np.arange(SIZE*3).reshape(SIZE,3).astype(np.float32)
b_np = np.arange(SIZE*3, SIZE*3+SIZE*3).reshape(SIZE,3).astype(np.float32)
c_np = np.zeros((SIZE*SIZE)).astype(np.float32)

# create the buffers to hold the values of the input
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=a_np)
b_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=b_np)
# create output buffer
c_buf = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, c_np.nbytes)

#Compilation
prg = cl.Program(ctx, source).build()

start = time.time()
# Kernel is now launched
launch = prg.elementwise(queue, (SIZE,SIZE), None, a_buf, b_buf, c_buf)
# wait till the process completes
launch.wait()
elem_wise_time = time.time()

##
# Reduction

red_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, np.array((1),dtype=np.float32).nbytes)
launch = prg.reduce(queue, (SIZE*SIZE,), None, c_buf,
    cl.LocalMemory(4*(np.dtype(np.float32).itemsize)),
    red_buf)
# wait till the process completes
launch.wait()
reduction_time = time.time()

cl.enqueue_read_buffer(queue, c_buf, c_np).wait()

red_np = np.empty((1)).astype(np.float32)
cl.enqueue_read_buffer(queue, red_buf, red_np).wait()

# print the output
# print "a:\n", a_np
# print "b:\n", b_np
# print "c:\n", c_np
# print "red:\n", red_np
# print "numpy:\n", np.sum(c_np)

print "elem_wise_time:", elem_wise_time-start
print "reduction_time:", reduction_time-elem_wise_time
print "Total:", reduction_time-start
