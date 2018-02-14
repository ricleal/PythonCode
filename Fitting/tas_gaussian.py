# -*- coding: utf-8 -*-
"""

Simple TAS parse and gaussian fit

=
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def gaussian(x, A, center, fwhm):
    '''
    Gaussian with fwhm and not sigma
    '''
    return A * np.exp(-4 * np.log(2) * (x - center)**2 / fwhm**2)


#
# Data
#
# Gaussian parameters
data = np.loadtxt("tas.txt")
x = data[:, 0]
y = data[:, 1]

# Guess for  A, center, fwhm from the y_noise!
#
A = np.max(y) - np.min(y)
center = np.sum(x*y)/np.sum(y)
sigma = np.sqrt(np.abs(
    np.sum((x-center)**2 * y)/np.sum(y)
))

fwhm = sigma * np.sqrt(8*np.log(2))
print("Using guess:   A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    A, center, fwhm, sigma))

#
# Fitting
#

init_values = [A, center, fwhm]     # for [amp, cen, wid]
coefficients, _ = curve_fit(gaussian, x, y, p0=init_values)
sigma = coefficients[2] / np.sqrt(8*np.log(2))
print("Fitted Coeffs: A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    coefficients[0], coefficients[1], coefficients[2], sigma))

x_fit = np.arange(x.min(), x.max(), 0.1)
y_fit = gaussian(x_fit, *coefficients)

plt.figure()
plt.plot(x, y, '-', label="Data")
plt.plot(x_fit, gaussian(x_fit, A, center, fwhm), '-', label="Guess")
plt.plot(x_fit, y_fit, '-', label="Fit")
plt.legend()
plt.show()
