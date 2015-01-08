#!/usr/bin/env python

"""
Run as:

python setup.py build_ext --inplace


Or, instead of using this file, the following should also work:
#
cython fib.pyx

# Compile the object file   
gcc -c -fPIC -I/usr/include/python2.7/ fib.c

# Link it into a shared library
gcc -shared fib.o -o fib.so

"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("fib.pyx"),
)
