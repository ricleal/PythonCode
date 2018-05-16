from __future__ import absolute_import
import pycuda.driver as cuda
import pycuda.autoinit
import numpy
import numpy.linalg as la
from pycuda.compiler import SourceModule

number_of_threads = 16
block_size = 32
grid_size = 33

total_size = number_of_threads*block_size*grid_size
dtype = numpy.float32

a = numpy.random.randn(total_size).astype(dtype)
b = numpy.random.randn(total_size).astype(dtype)

a_gpu = cuda.to_device(a)
b_gpu = cuda.to_device(b)
c_gpu = cuda.mem_alloc(a.nbytes)

from jinja2 import Template

tpl = Template("""
    __global__ void add(
            {{ type_name }} *tgt, 
            {{ type_name }} *op1, 
            {{ type_name }} *op2)
    {
      int idx = threadIdx.x + 
        {{ block_size }} * {{number_of_threads}}
        * blockIdx.x;

      {% for i in range(number_of_threads) %}
          {% set offset = i*block_size %}
          tgt[idx + {{ offset }}] = 
            op1[idx + {{ offset }}] 
            + op2[idx + {{ offset }}];
      {% endfor %}
    }""")

rendered_tpl = tpl.render(
    type_name="float", number_of_threads=number_of_threads,
    block_size=block_size)

mod = SourceModule(rendered_tpl)
# end

func = mod.get_function("add")
func(c_gpu, a_gpu, b_gpu,
     block=(block_size, 1, 1),
     grid=(grid_size, 1))

c = cuda.from_device_like(c_gpu, a)

assert la.norm(c-(a+b)) == 0
