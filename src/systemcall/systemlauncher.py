#!/usr/bin/python

'''
Created on Aug 9, 2013

@author: leal

Launcher to run shell commands.



'''
import subprocess
import threading
import time
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Launcher(threading.Thread):
    '''
    Launcher class.
    
    It only Inherits from Thread for time out purposes.
    
    The main method : launch() is blocker
    
    '''

    def __init__(self,command,timeout):
        '''
        Constructor
        @param command: Shell commands
        @param timeout: Timeout
         
        '''
        
        threading.Thread.__init__(self)
        self.__command = command
        self.__timeout = timeout
        logger.debug("Command to execute <%s> with timeout=%d"%(command,timeout))
        
        self.__out = None
        self.__err = None
        self.__process = None
        self.__pid = None
        self.__returnCode = None
    
    def __str__(self):
        return "Launcher: " + self.__command + "; timeout=%d"%self.__timeout
    
    def __repr__(self):
        return self.__str__()
    
    def run(self):
        '''
        Overrides: threading.Thread
        
        Executed through a thread
        
        Communicate  blocks until the command is fully executed.
        '''
        
        logger.debug("Running in background: %s" % self.__command)        

        self.__process = subprocess.Popen(self.__command,
                              shell=True,
                              stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        
        self.__pid = self.__process.pid
        self.__out, self.__err = self.__process.communicate()
        self.__returnCode = self.__process.returncode
        
    ### Non private methods:
    
    def launch(self):
        """
        Only function to be called. Starts the command with a time out.
        
        Blocks the execution!!!!
        
        It might have to be launched within other thread!!!!
        http://stackoverflow.com/questions/4158502/python-kill-or-terminate-subprocess-when-timeout
        """
        self.start()
        self.join(self.__timeout)

        if self.is_alive():
            logger.info("Thread timed out but the process is still running. Killing: %s" % self.__command )
            self.__process.terminate()
            self.join()
            logger.debug("Done.")
        else :
            logger.info("Thread finished successfully: %s"%self.__command)
    
    def isSubProcessRunning(self):
        """
        Just checks if the thread is running.
        """    
        # Check if child process has terminated. Set and return returncode attribute.
        if self.__process.poll() is None:
            return True
        else:
            return False
    
    def kill(self):
        if self.is_alive():
            logger.debug("Thread is alive... Killing subprocess: %s"%self.__command)
            self.__process.terminate()
            self.join()
            logger.debug("Process killed...")
        
    
    def pid(self):
        if self.__pid is not None:
            return self.__pid
        else:
            logger.error("SubProcess / Pid is None!")
    
    def exit(self):
        self.__process.terminate()
        self.join()
            
    def error(self):
        return self.__err
    
    def output(self):
        return self.__out
    
    def returnCode(self):
        return self.__returnCode
    
    def __del__(self):
        self.kill()




    