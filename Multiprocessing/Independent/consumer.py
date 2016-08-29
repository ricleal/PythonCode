#!/usr/bin/env python

import os
import sys
import psutil

'''
'''


if __name__ == '__main__':
    if len(sys.argv != 2):
        print "Usage %s <pid>"%sys.argv[0]
    else:
        pid = sys.argv[1]
        p = psutil.Process(pid)
