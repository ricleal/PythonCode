import multiprocessing as mp
import time
import os
import random

random.seed(123)

n_processes = os.cpu_count() - 4

limit = 10

def cycle(offset):
    time.sleep(0.1)
    # return random.randint(offset, offset + limit)
    return random.randint(0, 100)

def worker(queueIn: mp.Queue, queueOut: mp.Queue):
    while True:
        offset = queueIn.get()
        if offset == -1:
            break
        ret = cycle(offset)
        queueOut.put(ret)
        print(f"Worker {os.getpid()}: {offset} -> {ret}")
        if ret == 0:
            break



def main():
    queueIn = mp.Queue()
    queueOut = mp.Queue()
    pool = mp.Pool(n_processes, worker,(queueIn, queueOut, ))
    
    offset = 0
    for i in range(n_processes):
        queueIn.put(offset)
        offset += limit

    ret = queueOut.get()
    while ret != 0:
        queueIn.put(offset)
        offset += limit
        ret = queueOut.get()
        print(f"Main: {ret}")

    # send the stop signal to the workers
    for i in range(n_processes-1):
        queueIn.put(-1)
    


    print("Closing the pool")
    pool.close()
    print("Joining the pool")
    pool.join()
    print("Pool closed and joined")

    print("QueueIn size: ", queueIn.qsize())
    print("QueueOut size: ", queueOut.qsize())
    
    queueIn.close()
    queueOut.close()
    print("Queues closed")

    print("Main process finished")


if __name__ == "__main__":
    main()