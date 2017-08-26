from multiprocessing import Process, Queue, Manager
from multiprocessing.managers import BaseManager  
import random
import time


'''
This one works using a shared object through a Manager.
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

class CustomTable(object):
    def __init__(self):
        self.contents = []
    
    def addItem(self, item):
        self.contents.append(item)
    
    def display(self):
        print(self.__repr__)
    
    def __repr__(self):
        res = 80*"-" + "\n" + str(self.contents) + "\n" + 80*"-" + "\n"
        return res

class CustomTableManager(BaseManager):  
    pass  

CustomTableManager.register('CustomTable', CustomTable, exposed = ['contents', 'addItem', 'display', '__repr__'])  

customTableManager = CustomTableManager()  
customTableManager.start()  

class Display(object):
    def __init__(self):
        # self.tasks = CustomTable()
        self.tasks = customTableManager.CustomTable()

    def display_tasks(self, n_tasks=10):
        def add_task(task):
            self.tasks.addItem(task)
            print("Dislaying tasks so far:\n{}".format(self.tasks))
        Scheduler().start(add_task, n_tasks)
        print("Total tasks:\n{}".format(self.tasks))

Display().display_tasks(5)