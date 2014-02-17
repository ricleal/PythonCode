'''
Created on Feb 17, 2014

@author: leal
'''
import unittest

from communicate import Communicate

class TestCommunicate(unittest.TestCase):

    executable = '/net/serhom/home/cs/richard/Free_Lamp81/START_lamp -nws'
    prompt = "loaded ..."
    exitCommand = "exit"
    
    stringToPrint = "Hello, Python"
    
    def setUp(self):
        pass

    def test_lamp_simple_print(self):
        lamp = Communicate(self.executable, self.prompt, self.exitCommand)
        #time.sleep(0.2)
        output,errors = lamp.communicate('print, "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0.2)
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        lamp.exit();
        
    def test_lamp_print_with_process_relaunch(self):
        lamp = Communicate(self.executable, self.prompt, self.exitCommand)
        #time.sleep(0.2)
        output,errors = lamp.communicate('print, "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0.2)
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        lamp.exit();
        
        output,errors = lamp.communicate('print, "%s"'%self.stringToPrint, waitTimeForTheCommandToGiveOutput=0.2)
        
        self.assertEqual(output.strip(),self.stringToPrint)
        self.assertEqual(errors.strip(),"")
        
        lamp.exit();
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()