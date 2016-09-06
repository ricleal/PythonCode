#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Code to test uncertainties and numpy masks!
'''
from uncertainties import unumpy
import numpy as np
import numpy.ma as ma

v = np.array([1,2,3,4,5,6,7,8,9,10])
e = np.sqrt(v)

un = unumpy.uarray(v,e)
print(un)
print("Mean array = {}.".format(v.mean()))
print("Mean uncertainties array = {}.".format(un.mean()))


mask = v%2==0
un_masked = ma.masked_array(un, mask=mask)
v_masked = ma.masked_array(v, mask=mask)
print(un_masked)
print("Mean array masked = {}.".format(v_masked.mean()))
print("Mean uncertainties array masked = {}.".format(un_masked.mean()))

assert(v.mean() ==  unumpy.nominal_values(un.mean()))
assert(v_masked.mean() ==  unumpy.nominal_values(un_masked.mean()))

assert(v.sum() ==  unumpy.nominal_values(un.sum()))
assert(v_masked.sum() ==  unumpy.nominal_values(un_masked.sum()))
