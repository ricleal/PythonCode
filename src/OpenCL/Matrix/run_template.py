'''
Created on Dec 23, 2014

@author: rhf

Based on http://compeng.uni-frankfurt.de/fileadmin/Arbeiten/jgerhard/PyOpenCL.pdf



'''

import pyopencl as cl
import numpy as np
import time
import sys


# 

class GPU():
    """
    General class to compile GPU code and call kernel methods
    """
    def __init__(self,sourceCodeFileName):
        self.sourceCodeFileName = sourceCodeFileName
    
    def _getSourceCode(self):
        """ Gives the src-code of the file passed in __init__"""
        try:
            srcFile = open(self.sourceCodeFileName, 'r')
        except IOError:
            print "Error: File does not appear to exist."
            sys.exit(-1)
        src = ''.join(srcFile.readlines())
        return src
    
    def init(self):
        """
        Inits the ctx and program
        """
        platform = cl.get_platforms()[0]
        try:
            mydevices = platform.get_devices(device_type=cl.device_type.GPU)
        except:
            mydevices = platform.get_devices(device_type=cl.device_type.ALL)
        mydevice = mydevices[0]
        ctx = cl.Context(mydevices)
        self.queue = cl.CommandQueue(ctx, device=mydevice)
        src = self._getSourceCode()
        self.prg = cl.Program(ctx, src).build()
        self.ctx = ctx
    
    def callFunction(self,funcName,*args):
        """
        Calls a kernel function funcname
        """
        methodToCall = getattr(self.prg, funcName)
        methodToCall(self.queue, *args)
        return args
        
        


matrix1 = 1 * np.random.random((16,16)).astype(np.float32)
matrix2 = 1 * np.random.random((16,16)).astype(np.float32)


##### 1
t0 = time.time()

gpu1 = GPU("matrix1.c")
gpu1.init()
            
mf = cl.mem_flags
a_buf = cl.Buffer(gpu1.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix1)
b_buf = cl.Buffer(gpu1.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix2)
dest_buf = cl.Buffer(gpu1.ctx, mf.WRITE_ONLY, matrix1.nbytes )

gpu1.callFunction("naive_mul", matrix1.shape, None,a_buf, b_buf, dest_buf)

final_matrix1 = np.empty_like(matrix1)
cl.enqueue_copy(gpu1.queue, final_matrix1 , dest_buf)

delta_t1 = time.time() - t0

print  "Matrix1:\n", final_matrix1

##### 2
t0 = time.time()

gpu2 = GPU("matrix2.c")
gpu2.init()
            
mf = cl.mem_flags
a_buf = cl.Buffer(gpu2.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix1)
b_buf = cl.Buffer(gpu2.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix2)
dest_buf = cl.Buffer(gpu2.ctx, mf.WRITE_ONLY, matrix1.nbytes )

gpu2.callFunction("local_mul", matrix1.shape, None, a_buf, b_buf, dest_buf)

final_matrix2 = np.empty_like(matrix1)
cl.enqueue_copy(gpu2.queue, final_matrix2 , dest_buf)

delta_t2 = time.time() - t0

print  "Matrix2:\n", final_matrix2


print "\n *** Are these two arrays similar?", np.allclose(final_matrix1, final_matrix2)
print "Times : t1 =", delta_t1*1000,"ms ; t2 =", delta_t2*1000 , "ms ; Method 2 is faster", delta_t1 / delta_t2, "times"
if __name__ == '__main__':
    pass