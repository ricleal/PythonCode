#!/usr/bin/python
# -*- coding: <encoding name> -*-

import resource
import h5py
import numpy as np

def mem():
    '''
    Return mem usage in MB
    '''
    usage=resource.getrusage(resource.RUSAGE_SELF)
    val = (usage[2]*resource.getpagesize())/1000000.0
    return val

print mem()
f = h5py.File('/SNS/MANDI/IPTS-12697/0/4089/NeXus/MANDI_4089_event.nxs', 'r')
print mem()
banks = [i for i in  f['entry'].keys() if i.startswith('bank') and not i.endswith('events') ]
print mem()

data = {}
for b in banks:
    d = f['entry'][b]['data_x_y']
    arr = np.zeros(d.shape, dtype=d.dtype)
    d.read_direct(arr)
    data[b]=d
    print mem()
