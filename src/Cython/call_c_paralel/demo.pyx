"""


"""
cimport numpy as cnp
import numpy as np

def getDummyMatrix( cnp.ndarray[cnp.float64_t, ndim=2] arr ):
    cdef int i,j
    outArr = np.empty_like(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            outArr[i,j] = i + j * arr[i,j]
    return outArr

def matMult1(cnp.ndarray[cnp.float64_t, ndim=2] A, cnp.ndarray[cnp.float64_t, ndim=2] B):
    print A.shape[0], B.shape[1]
    out = np.zeros( (A.shape[0], B.shape[1]), dtype=np.float64)
    
    # Take each row of A
    for i in range (0 , A.shape[0]):
        # And multiply by every column of B
        for j in range ( B.shape[1]):
            s = 0
            for k in range ( A.shape[1]):
                s += A [i,k] * B[k,j]
            out [i,j] = s
    return out

def matMult2( cnp.ndarray[cnp.float64_t, ndim=2] A,
              cnp.ndarray[cnp.float64_t, ndim=2] B, 
              cnp.ndarray[cnp.float64_t, ndim=2] out):
    cdef int i, j, k
    cdef cnp.float64_t s
    # Take each row of A
    for i in range (0 , A.shape[0]):
        # And multiply by every column of B
        for j in range (B.shape[1]):
            s = 0
            for k in range (A.shape[1]):
                s += A[i,k] * B[k,j]
            out[i,j] = s

def matMult_part( int start, int end,
                         cnp.ndarray[cnp.float64_t, ndim=2] A,
                         cnp.ndarray[cnp.float64_t, ndim=2] B, 
                         cnp.ndarray[cnp.float64_t, ndim=2] out):
    cdef int i, j, k
    cdef cnp.float64_t s
    with nogil:
        # Take a selected few rows from A
        for i in range(start, end):
            # And multiply each column of B
            for j in range (B.shape [1]):
                s = 0
                for k in range ( A.shape[1]):
                    s += A [i, k] * B [k, j]
                out [i, j] = s

                