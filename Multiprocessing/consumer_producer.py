from multiprocessing import Process, Queue
import random
import time

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

        workers = [
            Process(
                target=self.produce,
                args=(i,)
            )
            for i in range(self.NUMBER_OF_WORKERS)
        ]

        for w in workers:
            w.start()
        for w in workers:
            w.join()

        self.queue.put(None)
        consumer.join()

Manager().start()