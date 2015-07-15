import timing

"""
Inspired from: http://joelgrus.com/2015/07/07/haskell-style-fibonacci-in-python/

"""
N = 25
the_list = range(N)

###################
def fib_slow(n):
  """the profoundly inefficient recursive implementation"""
  if n in [0, 1]:
    return 1
  else:
    return fib_slow(n - 1) + fib_slow(n - 2)

@timing.timed
def test_fib_slow():
    map(fib_slow, the_list)

###################

def fib_iterative(n):
  """the iterative implementation"""
  x, y = 0, 1
  for _ in range(n):
    x, y = y, x + y
  return y

@timing.timed
def test_fib_iterative():
    map(fib_iterative, the_list)

####################
from itertools import islice

def tail(iterable):
  """return elements from 1 to forever"""
  return islice(iterable, 1, None)

def take(n, iterable):
  """return elements from 0 to n in a list"""
  return list(islice(iterable, 0, n))

def fibs_iter():
  x, y = (0, 1)
  while True:
    yield y
    (x, y) = (y, x + y)

@timing.timed
def test_fibs_iter():
    take(N, fibs_iter())

###################
from itertools import imap   # lazy map
from operator import add     # add(x, y) = x + y

def fibs_haskell():
  yield 1
  yield 1
  # In python 3: yield from map(add, fibs_haskell(), tail(fibs_haskell()))
  for n in imap(add, fibs_haskell(), tail(fibs_haskell())):
    yield n

@timing.timed
def test_fibs_haskell():
    take(N, fibs_haskell())
####################
from itertools import tee, izip

def fibs_tee():
    yield 1
    l, r = tee(fibs_tee())
    yield next(l)  # move forward
    while True:
        yield next(l)+next(r)

@timing.timed
def test_fibs_tee():
    take(N, fibs_tee())

##################
def fibs_haskell_tee():
  yield 1
  yield 1
  fibs1, fibs2 = tee(fibs_haskell_tee())
  # In python 3: yield from map(add, fibs1, tail(fibs2))
  for n in imap(add, fibs1, tail(fibs2)):
    yield n

@timing.timed
def test_fibs_haskell_tee():
    take(N, fibs_haskell_tee())

######################
if __name__ == '__main__':

    test_fib_slow()
    print "test_fib_slow:\t\t%f" % test_fib_slow.timed()

    test_fib_iterative()
    print "test_fib_iterative:\t%f" % test_fib_iterative.timed()

    test_fibs_iter()
    print "test_fibs_iter:\t\t%f" % test_fibs_iter.timed()

    test_fibs_haskell()
    print "test_fibs_haskell:\t%f" % test_fibs_haskell.timed()

    test_fibs_tee()
    print "test_fibs_tee:\t\t%f" % test_fibs_tee.timed()

    test_fibs_haskell_tee()
    print "test_fibs_haskell_tee:\t%f" % test_fibs_haskell_tee.timed()
