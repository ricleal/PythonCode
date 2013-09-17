'''
Created on Sep 17, 2013

@author: leal
'''

from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

CSV_FILE = "susy.csv"

data = np.genfromtxt(CSV_FILE, dtype=float, delimiter='\t', names=True) 
x1 = data["x1"]
y1 = data["y1"]
x2 = data["x2"]
y2 = data["y2"]

# Remove last three values from x2,y2 (they are nan!)
x2 = x2[:-3]
y2 = y2[:-3]

# interpolation
f1 = interp1d(x1, y1)
f2 = interp1d(x2, y2)

# new axis
xnew = np.linspace(max(min(x1),min(x2)), min(max(x1),max(x2)), len(x1)*2)

# x1,y1
fig1 = plt.figure()
fig1.canvas.set_window_title('X1,Y1')
ax1 = fig1.add_subplot(111)
ax1.plot(x1,y1,'o',label="data")
ax1.plot(xnew,f1(xnew),'-',label="interp")
ax1.legend()

#x2,y2
fig2 = plt.figure()
fig2.canvas.set_window_title('X2,Y2')
ax2 = fig2.add_subplot(111)
ax2.plot(x2,y2,'o',label="data")
ax2.plot(xnew,f2(xnew),'-',label="interp")
ax2.legend()

#y2-y1
fig3 = plt.figure()
fig3.canvas.set_window_title('Y2-Y1')
ax3 = fig3.add_subplot(111)
ax3.plot(xnew,f2(xnew)-f1(xnew),'-',label="interp")
ax3.legend()


plt.show()


if __name__ == '__main__':
    pass