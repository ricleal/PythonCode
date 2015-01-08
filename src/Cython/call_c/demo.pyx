"""
Call C functions
"""
from Cython.Shadow import NULL

# Example:
# Calling C library
cdef extern from "<gsl/gsl_sf_bessel.h>":
    double gsl_sf_bessel_J0 (double x)

cpdef double my_sf_bessel_J0(double x):
    return gsl_sf_bessel_J0(x)


#
# Calling external fle
#
cdef extern from "list.h":
    struct point:
        int    x
        int    y
    struct list_element:
        point * p
        list_element * next
    void list_push_front(list_element **list, point *p)
    void list_clean(list_element **list)
    void list_print(list_element *list)

# See main in list.c. It does the same
def test():
    cdef list_element *l = NULL
    cdef point p1
    p1.x = 1
    p1.y = 2
    cdef point p2
    p2.x = 3
    p2.y = 4
    cdef point p3
    p3.x = 5
    p3.y = 6

    list_push_front(&l, &p1)
    list_push_front(&l, &p2)
    list_push_front(&l, &p3)
    
    list_print(l)

    list_clean(&l)
 
    list_print(l)
    

