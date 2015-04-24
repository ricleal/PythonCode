# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:33:04 2015

@author: rhf
"""

import csv
import tabular as tb
import matplotlib.pyplot as plt
import numpy as np
import datetime

ELECT_PRICE_KW = 0.085
ELECT_SERVICE_FEE = 14
GAS_PRICE_THERM = 1.247
GAS_SERVICE_FEE = 6.65

data = tb.tabarray(SVfile='/home/rhf/Downloads/CSVReport.csv',
    delimiter=',', doublequote=True,)

data_elect = data[ data["Service Agreement Type"] == "E-RES" ]
data_gas = data[ data["Service Agreement Type"] == "G-RES" ]

fig = plt.figure(1)

dates = np.array(data_elect["Billing Period End"])
x = [datetime.datetime.strptime(i, "%m/%d/%Y" ) for i in dates]
y = data_elect["Consumption"]
ax1 = plt.subplot(211)
plt.plot(x, y, 'o')
for i,j in zip(x,y):
    ax1.annotate('$%.f'%(j*ELECT_PRICE_KW+ELECT_SERVICE_FEE), xy=(i,j),xytext=(5,0), textcoords='offset points')
plt.title("E-RES")
ax1.grid()
ax1.set_xlim([min(x) - datetime.timedelta(10,0),max(x) + datetime.timedelta(30,0)])
# rotate and align the tick labels so they look better
fig.autofmt_xdate()


dates = np.array(data_gas["Billing Period End"])
x = [datetime.datetime.strptime(i, "%m/%d/%Y" ) for i in dates]
y = data_gas["Consumption"]
ax2 = plt.subplot(212)
plt.plot(x, y, 'ro')
for i,j in zip(x,y):
    ax2.annotate('$%.f'%(j*GAS_PRICE_THERM+GAS_SERVICE_FEE), xy=(i,j),xytext=(5,0), textcoords='offset points')
plt.title("G-RES")
ax2.grid()
# rotate and align the tick labels so they look better
fig.autofmt_xdate()
ax2.set_xlim([min(x) - datetime.timedelta(10,0),max(x) + datetime.timedelta(30,0)])

plt.show()
