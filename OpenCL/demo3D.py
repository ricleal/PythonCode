import pyopencl as cl
import numpy as np

"""
OpenCL demo:



"""


source = """
__kernel void test(__global const float *a, __global const float *b, __global float *c)
{
    int i = get_global_id(0);
    int j = get_global_id(1);
    int k = get_global_id(2);
    
    int m = get_global_size(0);
    int n = get_global_size(1);
    int w = get_global_size(2);
    
    int idx = i*n*w + j*w + k; 
    
    c[idx] = a[idx] * b[idx];
}
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

a = [[[  1.,   2.,  1.],
      [  3.,   1.,  1.]],
     [[  1.,   9.,  1.],
      [  1.,   1.,  2.]]]
b = a

a_np = np.array(a, dtype=np.float32)
b_np = np.array(b, dtype=np.float32)
c_np = np.empty_like(a_np)

# create the buffers to hold the values of the input
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=a_np)
b_buf = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,hostbuf=b_np)
# create output buffer
c_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, c_np.nbytes)

#Compilation
prg = cl.Program(ctx, source).build()

# Kernel is now launched
launch = prg.test(queue, a_np.shape, None, a_buf, b_buf, c_buf)
# wait till the process completes
launch.wait()

cl.enqueue_read_buffer(queue, c_buf, c_np).wait()
# print the output
print "Shape:", a_np.shape
print "a:\n", a_np
print "b:\n", b_np
print "c:\n", c_np



