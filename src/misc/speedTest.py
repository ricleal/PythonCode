'''
Created on Nov 19, 2012

@author: leal
'''

import numpy as np
from datetime import datetime

def testSpectraIN5():
    nSpectra = 12 * 32 * 256
    nBinsTotal = nSpectra * 512;
    
    total = []
    for i in range(nBinsTotal):
        res = 500 * 500 + i
        total.append(res)
    
def testSpectraIN5np():
    nSpectra = 12 * 32 * 256
    nBinsTotal = nSpectra * 512;
    
    total = np.empty(nBinsTotal, dtype=float)
    for i in range(nBinsTotal):
        res = 500 * 500 + i
        total[i]=res
        
def testSpectraIN5npOpt():
    nSpectra = 12 * 32 * 256
    nBinsTotal = nSpectra * 512;
    
    # res = [0..nBinsTotal-1]
    res = np.arange(nBinsTotal, dtype=float)
    total = 500 * 500 + res  
    


if __name__ == '__main__':
    print "Main has started!"
    print "* testSpectraIN5"
    t_start = datetime.now()
    testSpectraIN5()
    t_end = datetime.now()
    t_total = t_end - t_start
    print "Total time: ", t_total, " seconds"
    print "* testSpectraIN5np"
    t_start = datetime.now()
    testSpectraIN5np()
    t_end = datetime.now()
    t_total = t_end - t_start
    print "Total time: ", t_total, " seconds"
    print "* testSpectraIN5npOpt"
    t_start = datetime.now()
    testSpectraIN5npOpt()
    t_end = datetime.now()
    t_total = t_end - t_start
    print "Total time: ", t_total, " seconds"
    print "Main has finished!"
