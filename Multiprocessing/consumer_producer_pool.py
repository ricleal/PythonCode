from multiprocessing import Process, Queue, cpu_count
import random
import time

'''
Implement my pool
Thanks: https://www.reddit.com/r/Python/comments/3z13vj/multiprocessing_question/?st=j6thstam&sh=bc4313ec

'''


TIMEOUT = 5


class Pool(object):
    """Very basic process pool with timeout."""

    def __init__(self, size=None, timeout=15):
        """Create new `Pool` of `size` concurrent processes.

        Args:
            size (int): Number of concurrent processes. Defaults to
                no. of processors.
            timeout (int, optional): Number of seconds to wait before
                killing the process.
        """
        self.size = size or cpu_count()
        self.timeout = timeout
        self.pool = []
        self._counter = 1
        self._q = Queue()

    def map(self, func, it):
        """Call `func` with each element in iterator `it`.

        Args:
            func (callable): Function/method to call.
            it (iterable): List of arguments to pass to each call of `func`.

        Returns:
            list: The results of all the calls to `func`.
        """
        while True:
            if len(it) and len(self.pool) < self.size:
                arg = it.pop(0)
                self._start_process(func, (arg,))
                continue

            if len(self.pool) == len(it) == 0:  # Finished
                break

            pool = []
            for proc in self.pool:
                if not proc.is_alive():
                    print('{} done.'.format(proc.name))
                    continue

                age = time.time() - proc.start_time
                if age >= self.timeout:
                    print('{} killed.'.format(proc.name))
                    proc.terminate()
                    continue

                pool.append(proc)

            self.pool = pool
            time.sleep(0.01)

        results = []
        while not self._q.empty():
            results.append(self._q.get())

        return results

    def _start_process(self, target, args):
        """Call `target` with `args` in a separate process.

        The result of the call is returned via `self._q`.

        Args:
            target (callable): Function to call in new process.
            args (it): Tuple/list of arguments to pass to `target`.

        """

        def _wrapper():
            """Closure around the callable."""
            result = target(*args)
            self._q.put(result)

        proc = Process(target=_wrapper,
                       name='Process#{}'.format(self._counter))
        proc.start()
        print('{} started.'.format(proc.name))
        proc.start_time = time.time()
        self.pool.append(proc)
        self._counter += 1
    


class Manager:
    def __init__(self):
        self.queue = Queue()
        self.NUMBER_OF_WORKERS = 10

    def consume(self):
        while True:
            task = self.queue.get()
            if task is None:
                self.queue.close()
                break
            time.sleep(0.05)
            print("Queue got task: {}.".format(task))
    
    def produce(self, value):
        time.sleep(random.uniform(0.1, 1.0))
        task = "TSK {}".format(value)
        self.queue.put(task)


    def start(self):

        consumer = Process(
            target=self.consume,
            args=(),
        )
        consumer.start()

        # workers = [
        #     Process(
        #         target=self.produce,
        #         args=(i,)
        #     )
        #     for i in range(self.NUMBER_OF_WORKERS)
        # ]

        p = Pool()
        p.map(self.produce, range(self.NUMBER_OF_WORKERS))


        # for w in workers:
        #     w.start()
        # for w in workers:
        #     w.join()

        self.queue.put(None)
        consumer.join()

Manager().start()