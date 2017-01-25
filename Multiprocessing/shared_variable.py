#!/usr/bin/env python
import os, sys, time
from multiprocessing import Pool

'''
Behaviour of sharing variables in multiprocessing

$ python shared_variable.py
('pid: ', 8122, 'x:', 23000, 'id(x):', 26091400, 'z:', [1], 'id(z):', 140082765015160)
1
('pid: ', 8123, 'x:', 23000, 'id(x):', 26091400, 'z:', [2], 'id(z):', 140082765015160)
2
('pid: ', 8125, 'x:', -23000, 'id(x):', 26656080, 'z:', [3], 'id(z):', 140082765015160)
3
('pid: ', 8124, 'x:', 23000, 'id(x):', 26091400, 'z:', [4], 'id(z):', 140082765015160)
4

$ python shared_variable.py  sleep
('pid: ', 8409, 'x:', 23000, 'id(x):', 15331208, 'z:', [1], 'id(z):', 140387323123832)
1
('pid: ', 8410, 'x:', 23000, 'id(x):', 15331208, 'z:', [2], 'id(z):', 140387323123832)
2
('pid: ', 8412, 'x:', -23000, 'id(x):', 15895888, 'z:', [3], 'id(z):', 140387323123832)
3
('pid: ', 8411, 'x:', 23000, 'id(x):', 15331208, 'z:', [4], 'id(z):', 140387323123832)
4

'''

x = 23000
z = []

def printx(y):
    global x
    if y == 3:
       x = -x
    z.append(y)
    print("pid: ", os.getpid(), "x:", x, "id(x):", id(x), "z:", z, "id(z):", id(z))
    print y
    if len(sys.argv) == 2 and sys.argv[1] == "sleep":
       time.sleep(.1) # should make more apparant the effect

if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map(printx, (1,2,3,4))
