import pyopencl as cl, numpy
import numpy.linalg as la

a = numpy.arange(16).astype(numpy.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

a_dev = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, size=a.nbytes)
cl.enqueue_write_buffer(queue, a_dev, a)

prg = cl.Program(ctx, """
#pragma OPENCL EXTENSION cl_intel_printf : enable
#pragma OPENCL EXTENSION cl_amd_printf : enable

__kernel void twice(__global float *a) {
    int i = get_local_id(0);
    int local_size = get_local_size(0);
    int group_id = get_group_id(0);
    a[i + local_size * group_id] *= 2;
    //a[i] = float(local_size);
    printf(" -> \n");
}
""").build()

prg.twice(queue, a.shape, (4,), a_dev)

result = numpy.empty_like(a)
cl.enqueue_read_buffer (queue, a_dev, result).wait()

print result
print len(result)
