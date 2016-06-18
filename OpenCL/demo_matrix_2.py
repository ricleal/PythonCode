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

//stride = step
#define BLOCK_SIZE 16
#define A_BLOCK_STRIDE (BLOCK_SIZE * n)
#define A_T_BLOCK_STRIDE (BLOCK_SIZE * m )

__kernel
void transpose(
    __global float *a,
    __global float *a_t ){

    __local float a_local[BLOCK_SIZE][BLOCK_SIZE];

    int m = get_global_size(0);
    int n = get_global_size(1);

    // int i = get_global_id (0);
    // int j = get_global_id (1);

    int grp_i = get_group_id (0);
    int grp_j = get_group_id (1);

    int lcl_i = get_local_id (0);
    int lcl_j = get_local_id (1);

    int base_idx_a = grp_i * BLOCK_SIZE + grp_j * A_BLOCK_STRIDE;
    int base_idx_a_t = grp_j * BLOCK_SIZE + grp_i * A_T_BLOCK_STRIDE;

    int glob_idx_a = base_idx_a + lcl_i + n * lcl_j;
    int glob_idx_a_t = base_idx_a_t + lcl_i + m * lcl_j;

    a_local[lcl_j][lcl_i] = a[glob_idx_a];
    barrier (CLK_LOCAL_MEM_FENCE);

    a_t[glob_idx_a_t] = a_local[lcl_i][lcl_j];
}
""").build()

a_t = np.empty_like(a).reshape((n,m))
a_t_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, a_t.nbytes)

with Timer('GPU'):
    prg.transpose(queue, a.shape, workgroup_size, a_buf, a_t_buf)
    cl.enqueue_read_buffer(queue, a_t_buf, a_t).wait()

# print "a:\n", a
# print "aT:\n", a_t
