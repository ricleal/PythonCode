import pyopencl as cl, numpy
import numpy.linalg as la

a = numpy.arange(2**3).astype(numpy.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

a_dev = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, size=a.nbytes)
cl.enqueue_write_buffer(queue, a_dev, a)

prg = cl.Program(ctx, """
__kernel void twice(__global float *a) {
    int i = get_global_id(0);
    a[i] *= 2;
}
""").build()

prg.twice(queue, a.shape, (1,), a_dev)

result = numpy.empty_like(a)
cl.enqueue_read_buffer (queue, a_dev, result).wait()

assert la.norm(result-2*a) == 0
print result
