#!/usr/bin/python

'''
Created on August 2012

@author: ricardo.leal@ill.fr

Use this to look for nexus files in a directory. E.g. :

cd /net/serdon/illdata/121/in6
python ~/workspace/PyTests/src/print_nexus_sample.py '*.nxs'

'''

import nxs, os, sys
import numpy as np
import glob
'''



'''

def show(filename):

    print filename,
    f = nxs.open(filename)
    # /entry0
    f.opengroup('entry0')

   
    # /entry0/title
    f.opendata('title')
    print ' : ', f.getdata(),
    # /entry0
    f.closedata()
        
    # /
    f.closegroup()
    f.close()
    
    print
    
    
 

if __name__ == '__main__':
    
    if len(sys.argv) >= 2: 
        files = glob.glob(sys.argv[1])
        for file in files:
            show(file)
    else:
        print "Use: %s <Nexus file pattern>. Don't forget quotes to delimitate the file pattern!" % sys.argv[0]
        print "Eg: %s '*.nxs'" % sys.argv[0]

