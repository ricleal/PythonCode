#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Code to test uncertainties and numpy masks!
'''
from uncertainties import unumpy
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import pandas as pd

v = np.arange(16)
e = np.sqrt(v)
un = unumpy.uarray(v,e)
d = {'v' : v,
     'e': e,
     'un': un,
    }
df = pd.DataFrame(d)#, dtype='object')
print(df)
df.info()

#print(un)
print("Mean array = {}.".format(v.mean()))
print("Mean uncertainties array = {}.".format(un.mean()))
print("Mean uncertainties df values = {}.".format(df.un.values.mean()))

plt.figure()
plt.plot(unumpy.nominal_values(un),'o')

mask = v%2==0
un_masked = ma.masked_array(un, mask=mask)
v_masked = ma.masked_array(v, mask=mask)
#df.un = df.un.mask(mask)
df.un = df.un.mask(np.logical_not(mask), np.nan)
print(df)

#print(un_masked)
print("Mean array masked = {}.".format(v_masked.mean()))
print("Mean uncertainties array masked = {}.".format(un_masked.mean()))
print("Mean uncertainties df values masked = {}.".format(df.un.values.mean()))
print("NAN Mean uncertainties df values masked = {}.".format(np.nanmean(df.un.values)))

print(np.nanmean(unumpy.nominal_values(df.un.values)))


plt.figure()
plt.plot(unumpy.nominal_values(un_masked),'o')

assert(v.mean() ==  unumpy.nominal_values(un.mean()))
assert(v_masked.mean() ==  unumpy.nominal_values(un_masked.mean()))

assert(v.sum() ==  unumpy.nominal_values(un.sum()))
assert(v_masked.sum() ==  unumpy.nominal_values(un_masked.sum()))

#plt.show()

#
# Example nanmean not working
v = np.arange(16,dtype=np.float64)
e = np.sqrt(v)
v[1:3] = np.nan
e[1:3] = np.nan
print(v)
un = unumpy.uarray(v,e)
print(un)
print(un.mean())
print(np.nanmean(un))
print(v.mean())
print(np.nanmean(v))
print(np.isnan(un[1:3]))
