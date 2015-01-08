#!/usr/bin/env python

"""
Run as:

python setup.py build_ext --inplace

or

python setup.py build_ext --inplace --force


"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("demo",
              ["demo.pyx","list.c"],
              libraries=["m","gsl","gslcblas"]) # Unix-like specific
]

setup(
  name = "Demo App",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)