#!/usr/bin/env python

"""
First run:

python setup.py build_ext --inplace

Then:

python fib_run.py

"""

import demo

def main():
    
    # Test GSL
    print "my_sf_bessel_J0(5.0)", demo.my_sf_bessel_J0(5.0)
    
    #
    print demo.test()
    


if __name__ == "__main__":
    print "Main started..."
    main()
    print "Main ended!"
