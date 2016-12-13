
import pyopencl as cl
import numpy as np

"""

Multiply element by 1 square matrix and a vector of the same size

"""


source = """
// OpenCL version : c = a * b
__kernel void gpu_mul(__global const float *a, __global const float *b, __global float *c,
    const unsigned int m, const unsigned int n) {

    int i = get_global_id(0);
    int j = get_global_id(1);

    // Otherwise we could get m and n from:
    // int m = get_global_size(0);
    // int n = get_global_size(1);

    int idx = i*n + j;
    c[idx] = a[idx] * b[j];

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
a = np.arange(64, dtype=np.float32).reshape(8, 8)
b = np.ones(16, dtype=np.float32)*2
c = np.empty_like(a)

m,n = a.shape #Out[11]: (2, 3)

# create the buffers to hold the values of the input
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=a)
b_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=b)
# create output buffer
c_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, c.nbytes)

#Compilation
prg = cl.Program(ctx, source).build()

# Kernel is now launched
launch = prg.gpu_mul(queue, a.shape, None, a_buf, b_buf, c_buf,np.uint32(m),np.uint32(n))
# wait till the process completes
launch.wait()

cl.enqueue_read_buffer(queue, c_buf, c).wait()
# print the output
print "a:\n", a
print "b:\n", b
print "c:\n", c
