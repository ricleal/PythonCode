"""

Compile as: 
python setup.py build_ext --inplace

"""
from distutils.core import setup, Extension

# define the extension module
c_module = Extension('c_module', sources=['c_module.c'])

# run the setup
setup(ext_modules=[c_module])
