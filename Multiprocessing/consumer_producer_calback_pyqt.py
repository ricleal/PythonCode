from multiprocessing import Process, Queue, Manager
from multiprocessing.managers import BaseManager
import random
import time

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,\
    QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

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


# Display().display_tasks(5)

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.tableWidget = QTableWidget()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createTable()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        # button
        button = QPushButton('Start workers...', self)
        button.clicked.connect(self.on_click_button)
        self.layout.addWidget(button)

        self.setLayout(self.layout) 
 
        # Show widget
        self.show()
 
    def createTable(self):
        # self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.move(0,0)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
 
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
    @pyqtSlot()
    def on_click_button(self):
        print('PyQt5 button click')
        
        
        n_cols = self.tableWidget.columnCount()
        n_rows = self.tableWidget.rowCount()

        extra_rows = 10

        self.tableWidget.setRowCount(n_rows+extra_rows)
        for row in range(n_rows, n_rows+extra_rows):
            for col in range(n_cols):
                self.tableWidget.setItem(row,col, QTableWidgetItem("task row={} col={}".format(row,col)))

class AppManager(BaseManager):  
    pass 

AppManager.register('App', App, exposed = ['tableWidget'])  

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())