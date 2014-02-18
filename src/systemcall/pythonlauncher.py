#!/usr/bin/python

'''
Created on Aug 9, 2013

@author: leal

Launcher to run shell commands.



'''

import threading
import logging

logger = logging.getLogger(__name__)

class Launcher(threading.Thread):
    '''
    Launcher class.
    
    It only Inherits from Thread for time out purposes.
    
    The main method : launch() is blocker
    
    '''

    def __init__(self,pythonScript,timeout):
        '''
        Constructor
        @param command: Shell commands
        @param timeout: Timeout
         
        '''
        
        threading.Thread.__init__(self)
        self.__command = pythonScript
        self.__timeout = timeout
        logger.debug("Executing python script <%s> with timeout=%d"%(pythonScript,timeout))
        
        self.setDaemon(True) # kills substreads when exit
        
        self.variables= {}
        
            
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

        execfile(self.__command, self.variables )
        
        
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
            return {}
        else :
            logger.info("Thread finished successfully: %s"%self.__command)
            return self.variables
    




    