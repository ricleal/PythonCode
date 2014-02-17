'''
Created on Oct 17, 2013

@author: leal
'''

import Queue
import threading
import subprocess
import time
import os


class Communicate(object):
    '''
    Class to communicate asynchronously with a Linux process.
    '''


    def __init__(self, executable, prompt, exitCommand = None):
        """
        
        @param executable:
        @param prompt: Any string output when program has finished to start
        @param exitCommand: if there is a exit command
        """

        
        self._executable = executable
        self._prompt = prompt
        self._exitCommand = exitCommand
        
        self._launch()
        
        self._outQueue = Queue.Queue()
        self._errQueue = Queue.Queue()

        self._startThreads()
        self._startExecutable()
    
    def _startThreads(self):
        self.outThread = threading.Thread(target=self._enqueueOutput, args=(self._subproc.stdout, self._outQueue))
        self.errThread = threading.Thread(target=self._enqueueOutput, args=(self._subproc.stderr, self._errQueue))
        
        self.outThread.daemon = True
        self.errThread.daemon = True
        
        self.outThread.start()
        self.errThread.start()
    
    def _startExecutable(self):
        print self._executable, 'is starting...'
        output = self._getOutput(self._outQueue)
        while output.find(self._prompt) < 0:
            time.sleep(0.2)
            output = self._getOutput(self._outQueue)
        print self._executable, 'is starting... Done!'
        
        errors = self._getOutput(self._errQueue)
        print 'Errors while starting:'
        print errors
        

    def _enqueueOutput(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()
    
    def _getOutput(self, outQueue):
        outStr = ''
        try:
            while True:  # Adds output from the Queue until it is empty
                outStr += outQueue.get_nowait()
        except Queue.Empty:
            return outStr
    
    def send(self,command):
        self._relaunchIfItIsNotRunning()
        self._subproc.stdin.write(command + os.linesep)        
        self._subproc.stdin.flush()        
    
    def receiveOutput(self):
        output = self._getOutput(self._outQueue)
        return output
    
    def receiveErrors(self):
        errors = self._getOutput(self._errQueue)
        return errors
    
    def communicate(self,command,waitTimeForTheCommandToGiveOutput=0.2):
        print 'Executing:', command
        self.send(command)
        time.sleep(waitTimeForTheCommandToGiveOutput)
        return [self.receiveOutput(),self.receiveErrors()]
    
    def exit(self):
        """
        Try to send the exit command to subprocess running.
        Kill it if it is still running
        """
        if self._isSubProcessRunning() and self._exitCommand is not None:
            self._subproc.stdin.write(self._exitCommand)
            self._subproc.stdin.write(os.linesep)
            self._subproc.stdin.flush()
            time.sleep(0.5)
        
        if self._isSubProcessRunning() :
            self._subproc.kill()
        time.sleep(0.1)
        print 'Done!'
    
    def _launch(self):
        self._subproc = subprocess.Popen(self._executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    def _relaunchIfItIsNotRunning(self):
        if not self._isSubProcessRunning():
            self._launch()
            self._outQueue = Queue.Queue()
            self._errQueue = Queue.Queue()   
            self._startThreads()
            self._startExecutable()
    
    def _isSubProcessRunning(self):
        """
        Just checks if the thread is running.
        """    
        # Check if child process has terminated. Set and return returncode attribute.
        if self._subproc.poll() is None:
            return True
        else:
            return False

    def __del__(self):
        if self._isSubProcessRunning() :
            self.exit()    

    



class CommunicationThread(threading.Thread):
    def __init__(self):
        super(CommunicationThread, self).__init__()
        self.executable = '/net/serhom/home/cs/richard/Free_Lamp81/START_lamp -nws'
        self.prompt = "loaded ..."
        self.exitCommand = "exit"
    
    def run(self):
        self.lamp = Communicate(self.executable, self.prompt, self.exitCommand)
    
    def communicate(self,message):
        return self.lamp.communicate(message, waitTimeForTheCommandToGiveOutput=0.2)
        
    def join(self, timeout=None):
        super(CommunicationThread, self).join(timeout)

def test2():
    t = CommunicationThread()
    t.start()
    t.communicate('print, "Hello, Python"')

if __name__ == '__main__':
    #test2()
    pass
    
    
     
    
    
    