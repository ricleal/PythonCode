'''
Created on Feb 17, 2014

@author: leal
'''
import unittest
import threading
import time
import os

from systemlauncher import Launcher 

class Test(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_a_ShortCommandLongTimeoutSuccess(self):
        print
        l = Launcher('ls',2)
        l.launch()
        print "** Out:"
        print l.output()
        self.assertEqual(l.returnCode(),0)
    
    def test_b_ShortCommandLongTimeoutFailure(self):
        print
        l = Launcher('ls -la /root',2)
        l.launch()
        print "** Error:"
        print l.error()
        self.assertNotEqual(l.returnCode(),0)
    
    def test_c_LongCommandShortTimeout(self):
        print
        l = Launcher('sleep 10',1)
        l.launch()
        self.assertNotEqual(l.returnCode(),0)
        
    
    def test_d_AverangeCommandDoesntBlockCaller(self):
        print
        
        l = Launcher('sleep 2',10)
        
        # As launch block execution let's run in in a thread
        t = threading.Thread(target=l.launch)
        t.start()
        
        print "Doing something in launcher while command runs in bg..."
        time.sleep(0.1)
        pid = l.pid()
        os.system('ps -ef | grep %d'%pid)
        print "Pid of the subprocess:", pid
        time.sleep(0.5)
        self.assertTrue(l.isSubProcessRunning(), "Is subprocess running?")
        print "Still doing something in launcher while command runs in bg..."
        time.sleep(2)
        self.assertEqual(l.returnCode(),0)
        
        t.join()
    
    def test_e_realTimeOut(self):
        print
        data = {}
        data['command'] = 'sleep 10'
        data['timeout'] = 2
        
        l = Launcher(data['command'],data['timeout'])
        t = threading.Thread(target=l.launch)
        t.start()
        time.sleep(0.1)
        data['pid']=l.pid()
        
        while l.isSubProcessRunning():
            print 'Process is still running'
            time.sleep(0.2)
        t.join()
        
        data['out'] = l.output()
        data['err'] = l.error() 
        data['retCode'] = l.returnCode()
        self.assertNotEqual(l.returnCode(),0)
        print data    
        
    def test_f_realSuccess(self):
        print
        data = {}
        data['command'] = 'sleep 2'
        data['timeout'] = 10
        
        l = Launcher(data['command'],data['timeout'])
        t = threading.Thread(target=l.launch)
        t.start()
        time.sleep(0.1)
        
        data['pid']=l.pid()
        
        while l.isSubProcessRunning():
            print 'Process is still running'
            time.sleep(0.2)
        t.join()
        data['out'] = l.output()
        data['err'] = l.error() 
        data['retCode'] = l.returnCode()
        self.assertEqual(l.returnCode(),0)
        print data    
        
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)