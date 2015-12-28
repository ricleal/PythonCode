import pyopencl as cl
import numpy as np

"""
OpenCL demo:

Executes a multiplication in the GPU of 2 random vectors.

"""


source = """/**
//Traditional loop as a function in C:
void trad_mul(int n, const float *a, const float *b, float *c, int m, int n) {
    int i, j;
    for (i=0; i<m; i++)
        for (j=0; j<n; j++)
            c[i*m + j ] = a[i*m + j] * b[i*m + j];
}*/

// OpenCL version : c = a * b
__kernel void gpu_mul(__global const float *a, __global const float *b, __global float *c) {

    const int dim1 = get_global_size(0);
    const int dim2 = get_global_size(1);
    
    int id = get_global_id(0);
    c[id] = a[id] * b[id];
} // execute over n "work items"
"""


def get_prefered_context(preferedDeviceType = cl.device_type.GPU):
    """
    Assuming that only one platform is available! 
    """
    platforms = cl.get_platforms()
    if len(platforms) > 1:
        print "Warning : Several OpenCL platforms available! Using the first!"
    
    devices = platforms[0].get_devices(device_type=preferedDeviceType)
    if len(devices) > 1:
        print "Warning : Several OpenCL devices available! Using the first prefered type!"
    
    if devices is not None:
        thisDevice = devices[0]
        print "OpenCL : Using Platform",platforms[0].name ,"and device", thisDevice.name
        context = cl.Context(devices=[thisDevice])
    else:
        context = cl.create_some_context()
    return context

#Initialization phase:
#ctx = cl.create_some_context()
ctx = get_prefered_context()

queue = cl.CommandQueue(ctx) 

# create some data array to give as input to Kernel and get output
SIZE = 256
a_np = np.random.rand(SIZE).astype(np.float32)
b_np = np.random.rand(SIZE).astype(np.float32)
c_np = np.empty_like(a_np)

# create the buffers to hold the values of the input
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=a_np)
b_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=b_np)
# create output buffer
c_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, c_np.nbytes)

#Compilation
prg = cl.Program(ctx, source).build()

# Kernel is now launched
launch = prg.gpu_mul(queue, a_np.shape, None, a_buf, b_buf, c_buf)
# wait till the process completes
launch.wait()

cl.enqueue_read_buffer(queue, c_buf, c_np).wait()
# print the output
print "a:", a_np
print "b:", b_np
print "c :", c_np



