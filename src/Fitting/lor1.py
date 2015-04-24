# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:16:28 2015

@author: rhf
"""

import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def lorentz(p,x):
    numerator =  (p[0]**2 )
    denominator = ( x - (p[1]) )**2 + p[0]**2
    y = p[2]*(numerator/denominator)
    return y

def errorfunc(p,x,z):
    err = z - lorentz(p,x)
    return err

n_points = 25

p = np.array([0.1, 0, 2.0], dtype=np.double)
x = np.linspace(-1.5, 1.5, num=n_points, endpoint=True)
noise = np.random.randn(n_points) * 0.1
z = lorentz(p,x)
noisyz = z + noise

p0 = np.array([0.5,
               noisyz[np.where(noisyz==np.max(noisyz))], # index of max value
               np.max(noisyz)],
               dtype=np.double) #Initial guess
solp, ier = leastsq(errorfunc, 
                    p0, 
                    args=(x,noisyz),
                    Dfun=None,
                    full_output=False,
                    ftol=1e-9,
                    xtol=1e-9,
                    maxfev=100000,
                    epsfcn=1e-10,
                    factor=0.1)

plt.clf()
x_theory = np.linspace(-1.5, 1.5, num=n_points*5, endpoint=True)
z_theory = lorentz(p,x_theory)
plt.plot(x_theory, z_theory, 'k-', linewidth=1.5, alpha=0.6, label='Theoretical')
plt.scatter(x, noisyz, c='r', marker='+', color='r', label='Measured Data')
plt.plot(x, lorentz(solp,x), 'g--', linewidth=2, label='leastsq fit')
plt.xlim((-1.5, 1.5))
plt.ylim((-0.1, 2.1))
plt.grid(which='major')
plt.legend(loc=8)
plt.show()