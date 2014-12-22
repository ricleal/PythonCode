import pyopencl as cl
import numpy as np

source = """
kernel void demo(global int *res){ 
    res[get_global_id(0)] = get_local_id(0);
}"""

#Initialization phase:
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx) 

#Create mem object:
dout = cl.Buffer(ctx, 
                 cl.mem_flags.WRITE_ONLY, 
                 size = (1024 * np.dtype('int32').itemsize))

#Compilation phase:
prg = cl.Program(ctx, source).build()

#Execution phase:
event = prg.demo(queue, (1024, ), None, dout)
hout = np.empty((1024,), dtype = np.uint32)
event = cl.enqueue_read_buffer(queue, dout, hout).wait()

#Now do something with data on the host:
for element in hout:
    print element,
print