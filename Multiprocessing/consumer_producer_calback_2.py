from multiprocessing import Process, Queue, Manager
import random
import time

'''
This one works using a shared list among all the processes
'''
class Scheduler(object):
    def __init__(self):
        self.queue = Queue()

    def consume(self, call_back):
        while True:
            task = self.queue.get()
            if task is None:
                self.queue.close()
                break
            time.sleep(0.05)
            print("Queue got task: {}.".format(task))
            call_back(task)
            
    def produce(self, value):
        time.sleep(random.uniform(0.1, 1.0))
        task = "TSK {}".format(value)
        self.queue.put(task)


    def start(self, call_back, n_tasks=10):

        consumer = Process(target=self.consume, args=(call_back,))
        consumer.start()

        workers = [Process(target=self.produce,args=(i,))
            for i in range(n_tasks)]

        for w in workers:
            w.start()
        for w in workers:
            w.join()

        self.queue.put(None)
        consumer.join()


class Display(object):
    def __init__(self):
        manager = Manager()
        self.tasks = manager.list()
        # self.tasks = []
    
    def display_tasks(self, n_tasks=10):
        def add_task(task):
            self.tasks.append(task)
            print("Dislaying tasks so far: {}".format(self.tasks))
        Scheduler().start(add_task, n_tasks)
        print("Total tasks: {}".format(self.tasks))


Display().display_tasks(5)