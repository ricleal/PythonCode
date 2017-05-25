import multiprocessing
import ctypes
import threading

import numpy as np


class mp_counter(object):
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
    proc = threading.Thread(target=start_processes,kwargs={"counter":counter})
    proc.daemon = True
    proc.start()
    proc.join()