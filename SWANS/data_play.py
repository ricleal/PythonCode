
from struct import unpack
import matplotlib.pyplot as plt
import numpy as np


file_path = "/SNS/VULCAN/IPTS-16013/shared/SANS_detector/RUN80814.dat"

f = open(file_path,'rb')

f.seek(0) # start
raw = f.read(2**30)     # 1Gb Max
print "Last Position: %d" % f.tell()
f.close()

number_of_events = (len(raw)/8)
print "Number of Events:", number_of_events

# Unpacking: conversion from C to Python
# I =  unsigned int, 4 bytes = 32 bits
data = np.array(unpack("II"*number_of_events,raw), dtype=np.uint32)
print "Data length =", len(data)

# even positions are TOF
pp = data[::2]>1e9
npp = data[::2]<1e9
# See how many are true
print ">1e9:", np.sum(pp),"<1e9:",np.sum(npp)

# TOF only for data where TOF > 1e9
tof = (data[::2]-1e9*pp)*0.1
print "TOF Range: [",tof.min(),tof.max(), "] microseconds. Shape:", tof.shape

#
# Binning
#
plt.figure("Events for TOF <1e9")
bin_width = 100       #microseconds
bin_start = 0     #microseconds     
bin_end = 60000     #microseconds
print "Binning:", bin_start,bin_end,bin_width
hist, bin_edges = np.histogram(tof[npp],bins=np.arange(bin_start,bin_end,bin_width))
plt.plot(bin_edges[:-1], hist, '.')
plt.xlim(min(bin_edges), max(bin_edges))
plt.xlabel("Time (microseconds)")

#
# Plot detector
#
# slicing: start:stop:step
detector_indices = data[1::2]-400000
print "Detector indices: %d - %d. Total positions = %d"%(detector_indices.min(),detector_indices.max(),128*128)
x = detector_indices/128
y = np.mod(detector_indices,128)

plt.figure()
tof_low = 10000
tof_high = 30000
tof_filter = tof>tof_low
tof_filter *= tof<tof_high
t = np.histogram2d(x[npp*tof_filter],y[npp*tof_filter],bins=128)
plt.imshow(t[0].transpose(),vmax=None)
plt.colorbar()

#
#
#

plt.figure()
r = np.zeros(128)
r = []
for i in t[1][:-1]:
    for j in t[2][:-1]:
        r.append(np.sqrt(i*i+j*j))
s = t[0].flatten()
print len(r),len(s)
zb = plt.hist(r,weights=s,bins=128)



plt.show()



