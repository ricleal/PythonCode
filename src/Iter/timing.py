"""
some simple things to time
From: https://github.com/ricleal/Scipy2015HighPerformanceComputingTutorial/blob/master/Untitled3.ipynb

"""
import time


def _list_comprehension(N):
    return [x*x for x in xrange(N)]


def _for_append(N):
    L = []
    for x in xrange(N):
        L.append(x*x)
    return L


def _for_setitem(N):
    L = [None]*N
    i = 0
    for x in xrange(N):
        L[i] = x*x
        i += 1
    return L


def timed(f):
    def dec(*args, **kwds):
        start = time.time()
        res = f(*args, **kwds)
        dec.__time__[f.__name__] = time.time() - start
        return res
    def get_time():
        return dec.__time__.values()[0]
    dec.__time__ = {}
    dec.timed = get_time
    return dec


def compare(f1, f2, N, M=1000):
    t1 = 0; t2 = 0
    for i in xrange(M):
        f1(N)
        t1 += f1.timed()
    for i in xrange(M):
        f2(N)
        t2 += f2.timed()
    print "ratio: %s" % (t1/t2)



if __name__ == '__main__':
    N = 10000

    print("size = %s" % N)
    start = time.time()
    _list_comprehension(N)
    end = time.time() - start
    print("%s: list comp" % end)

    start = time.time()
    _for_append(N)
    end = time.time() - start
    print("%s: for append" % end)

    start = time.time()
    _for_setitem(N)
    end = time.time() - start
    print("%s: for setitem" % end)


# EOF
