"""
First run:

python setup.py build_ext --inplace

Then:

python fib_run.py

"""

import fib

print "Fib result:", fib.fib(2000)

print "Integration result of f:", fib.integrate_f(10,50,100)