# -*- coding: utf-8 -*-

'''


'''

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

from multiprocessing import Process, Queue
import random

def approximate_pi(repeats, queue):
    """
    Monte Carlo simulation to approximate pi.
    """
    inside = 0
    for _ in range(repeats):
        x, y = random.random(), random.random()
        if (((0.5 - x) ** 2) + ((0.5 - y) ** 2)) <= 0.25:
            inside += 1
    queue.put((4 * inside) / float(repeats) )



if __name__ == '__main__':
    jobs = []
    for i in [10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7, 10**7]:
        job = {}
        queue = Queue()
        p = Process(target=approximate_pi, args=(i, queue, ))
        job["arg"] = i
        job["process"] = p
        job["queue"] = queue
        jobs.append(job)
        p.start()

    for job in jobs:
        job["process"].join()

        print "Job: %s\tPid: %s\tExit code: %s\tInput param: %s\tResult %.10f"%(
            job["process"].name,
            job["process"].pid,
            job["process"].exitcode,
            job["arg"],
            job["queue"].get()
        )
