import pyopencl as cl
import numpy as np
from timer import Timer

'''
transpose Matrix mxn
m rows
n columns

Not optimised!!
'''

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

m = 2**13
n = 2**13

#workgroup_size = None
# Slow
# workgroup_size = (1,1)
workgroup_size = (2**4,2**4)

a = np.arange(m * n, dtype=np.float32).reshape((m,n))
a_buf = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, size=a.nbytes)
cl.enqueue_write_buffer(queue, a_buf, a)

prg = cl.Program(ctx, """
__kernel
void transpose(
    __global float *a,
    __global float *a_t ){

    int m = get_global_size(0);
    int n = get_global_size(1);

    int i = get_global_id (0);
    int j = get_global_id (1);

    int read_idx = j + i * n;
    int write_idx = i + j * m;

    a_t[write_idx] = a[read_idx];
    //a_t[read_idx] = write_idx;
}
""").build()

a_t = np.empty_like(a).reshape((n,m))
a_t_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, a_t.nbytes)

with Timer('GPU'):
    prg.transpose(queue, a.shape, workgroup_size, a_buf, a_t_buf)
    cl.enqueue_read_buffer(queue, a_t_buf, a_t).wait()

# print "a:\n", a
# print "aT:\n", a_t
