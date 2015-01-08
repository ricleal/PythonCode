"""
Fibonnaci function
"""

def fib(n):
    """
    Print the Fibonacci series up to n.
    """
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b

## Other example:

cdef double f(double x) except? -2:
    """ function to integrate """
    return x**2-x

def integrate_f(double a, double b, int N):
    cdef int i
    cdef double s, dx
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f(a+i*dx)
    return s * dx