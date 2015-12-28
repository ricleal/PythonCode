'''
Created on Feb 17, 2014

@author: leal
'''
import unittest
import threading
import time
import os

from pythonlauncher import Launcher 

class Test(unittest.TestCase):
    
    tmpfile = '/tmp/test12324.py'
    
    def setUp(self):
        f = open(self.tmpfile, 'w')
        f.write("import time\n")
        f.write("print 'Starting...'\n")
        f.write("a = 1\n")
        f.write("time.sleep(2)\n")
        f.write("b = 2\n")
        f.write("if locals().has_key('c'):\n")
        f.write("\tc=True\n")
        f.write("print 'Finishing...'\n")

    def test_longer_time_out(self):
        
        l = Launcher(self.tmpfile,5)
        vglobal,vlocal = l.launch()
        self.assertFalse(vglobal.has_key('a'))
        self.assertEqual(vlocal['a'],1)
    
    def test_shorter_time_out(self):
        
        l = Launcher(self.tmpfile,0.1)
        vglobal,vlocal  = l.launch()
        self.assertEqual(vlocal,{})
        self.assertEqual(vglobal,{})
    
    def test_mixing_out_values(self):
    
        vglobal={}
        vlocal={}
        vlocal['a']=2
        self.assertEqual(vlocal['a'],2)
        self.assertEqual(vglobal,{})
        # short time out
        l = Launcher(self.tmpfile,0.1)
        gv,lv = l.launch()
        vlocal.update(lv)
        self.assertEqual(vlocal['a'],2)
        self.assertEqual(vglobal,{})
        #long time out
        vlocal['c']=1
        l = Launcher(self.tmpfile,3)
        gv,lv = l.launch(localVariables=vlocal)
        self.assertEqual(l.getOutput(),'Starting...\nFinishing...\n')
        vlocal.update(lv)
        self.assertEqual(vlocal['a'],1)
        self.assertTrue(vlocal['c'])
        self.assertNotEqual(gv, {})
        
        
    
    def test_from_caller_thread(self):
                
        l = Launcher(self.tmpfile,10)
        # As launch block execution let's run in in a thread
        t = threading.Thread(target=l.launch)
        t.start()
        
        while l.is_alive() :
            print "Waiting.."
            time.sleep(0.1)
        
        ret = l.localVariables
        t.join()
        self.assertEqual(ret['a'],1)
        
    def tearDown(self):
        os.remove(self.tmpfile)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWriter']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)