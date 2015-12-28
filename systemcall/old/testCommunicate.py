'''
Created on Feb 17, 2014

@author: leal
'''
import unittest
import time

from communicate import Communicate

class TestCommunicate(unittest.TestCase):

    lampExecutable = '/net/serhom/home/cs/richard/Free_Lamp81/START_lamp -nws'
    lampPrompt = "loaded ..."
    lampExitCommand = "exit"
    stringToPrint = "Hello, Python"
    
    pythonExecutable = '/usr/bin/python'
    pythonPrompt = ""
    pythonExitCommand = "exit()"
    
    def setUp(self):
        pass

    def test_lamp_simple_print(self):
        lamp = Communicate(self.lampExecutable, self.lampPrompt, self.lampExitCommand)
        
        output,errors = lamp.communicate('print, "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0.2)
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        lamp.exit();
        
    def test_lamp_print_with_process_relaunch(self):
        lamp = Communicate(self.lampExecutable, self.lampPrompt, self.lampExitCommand)
        #time.sleep(0.2)
        output,errors = lamp.communicate('print, "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0.2)
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        lamp.exit();
        
        output,errors = lamp.communicate('print, "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0.2)
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        lamp.exit();
 
    def test_python_simple_print(self):
        '''
        To run just this test:
        python -m unittest -q testCommunicate.TestCommunicate.test_python_simple_print
        '''

        pyshell = Communicate(self.pythonExecutable, self.pythonPrompt, self.pythonExitCommand)
        time.sleep(0.2)
        output,errors = pyshell.communicate('print "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0)
        
        print 'O', output
        print 'E', errors
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        pyshell.exit();

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()