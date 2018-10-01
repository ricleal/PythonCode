import ctypes
import multiprocessing
import threading

import numpy as np

'''
It increments an array by 1

Example:
$ python3 shared_array_2.py 
Before: [1.0, 2.0, 3.0, 4.0]
After:  [2. 3. 4. 5.]

'''

class mp_counter(object):
    '''
    Shared array counter in memory with a lock
    '''

    def __init__(self, initval=0):
        shared_array_base = multiprocessing.Array(ctypes.c_double, initval)
        self.val = np.ctypeslib.as_array(shared_array_base.get_obj())
        self.lock = multiprocessing.Lock()

    def increment(self):
        with self.lock:
            self.val += 1

    def decrement(self):
        with self.lock:
            self.val -= 1

    def value(self):
        with self.lock:
            return self.val


def start_processes(counter):
    print("Before:", counter)
    m = mp_counter(counter)
    m.increment()
    print("After: ", m.value())


if __name__ == '__main__':
    counter = [1., 2., 3., 4.]
    proc = threading.Thread(target=start_processes,
                            kwargs={"counter": counter})
    proc.daemon = True
    proc.start()
    proc.join()
