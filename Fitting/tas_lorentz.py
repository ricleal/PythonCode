# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def lorentzian(x, A, center, fwhm):
    '''
    Lorentzian with fwhm and not sigma
    '''
    # return 2*A/np.pi * fwhm / (4*(x-center)**2 + fwhm**2)
    # return A / (1 +((x-center)/fwhm)**2)
    # return A * ( (fwhm/2) / ((x-center)**2 + (fwhm/2)**2)  )
    return A * ((fwhm/2) / ((x-center)**2 + (fwhm/2)**2))


#
# Data
#
# Gaussian parameters
data = np.loadtxt("tas.txt")
x = data[:, 0]
y = data[:, 1]

#
# Guess for  A, center, fwhm from the y!
#
A = np.max(y) - np.min(y)
center = np.sum(x*y)/np.sum(y)
sigma = np.sqrt(np.abs(
    np.sum((x-center)**2 * y)/np.sum(y)
))

fwhm = 2 * sigma
print("Using guess:   A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    A, center, fwhm, sigma))

#
# Fitting
#
init_values = [A, center, fwhm]     # for [amp, cen, wid]
coefficients, _ = curve_fit(lorentzian, x, y, p0=init_values)
sigma = coefficients[2] / 2
print("Fitted Coeffs: A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    coefficients[0], coefficients[1], coefficients[2], sigma))

x_fit = np.arange(x.min(), x.max(), 0.1)
y_fit = lorentzian(x_fit, *coefficients)

plt.figure()
plt.plot(x, y, '-', label="Perfect")
# plt.plot(x, y, '.', label="noise")
plt.plot(x_fit, lorentzian(x_fit, A, center, fwhm), '-', label="Guess")
plt.errorbar(x, y, yerr=np.sqrt(y), fmt='.', label="Data")
plt.plot(x_fit, y_fit, '-', label="Fit")
plt.legend()
plt.show()
