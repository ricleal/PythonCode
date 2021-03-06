#!/usr/bin/python

'''
@author: Ricardo Leal
'''
import time
import threading
from datetime import datetime

# Lock
lock = threading.Lock()


def threadSafeFunc1(i):
    ''' Function to be threaded '''
    print "Tread %d is doing NON critical stuff" % i
    time.sleep(0.5)
    
    lock.acquire()
    print "Tread %d is doing critical stuff"% i
    time.sleep(0.5)
    print "Tread %d has finished doing critical stuff" % i 
    lock.release()

def threadSafeFunc2(i):
    ''' Function to be threaded '''
    print "Tread %d is doing NON critical stuff" % i
    time.sleep(0.5)
    with lock:
        print "********************************"
        print "Tread %d is doing critical stuff"% i
        time.sleep(0.5)
        print "Tread %d has finished doing critical stuff" % i 
        


if __name__ == '__main__':
    
    t_start = datetime.now()    
    
    thread_list = []

    for i in range(10):
        print "Launching thread: ", i
        t = threading.Thread(target=threadSafeFunc2, args=(i,))
        # Put threads in a list        
        thread_list.append(t)
        
        # optional (rather than putting them on a list)
        # t.start()
    
    # Start all threads
    [x.start() for x in thread_list]

    print "Waiting for the threads to do their job!"
    # Wait for all of them to finish
    [x.join() for x in thread_list]
    
    print "Main: I haved waited for the threads to finish!"    
    
    t_end = datetime.now()
    t_total = t_end - t_start
    
    print "Total time: ", t_total
    print "Main has finished!"
