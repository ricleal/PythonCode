# -*- coding: utf-8 -*-
"""

Simple Gaussian coeffs estimation

$ python gaussian_guess.py 
Ideal:         A=5.00 center=5.00 fwhm=2.00 (sigma=0.85).
Using guess:   A=5.63 center=5.00 fwhm=1.52 (sigma=0.65).
Fitted Coeffs: A=4.99 center=4.95 fwhm=1.99 (sigma=0.84).
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
A = 5
center = 5
fwhm = 2

x = np.linspace(0, 10, 50)
y = gaussian(x, A, center, fwhm)
# Add random noise to the data
y_noise = y + np.random.normal(0, 0.3, len(y))
y_error = np.sqrt(np.abs(y_noise))

sigma = fwhm / np.sqrt(8*np.log(2))
print("Ideal:         A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    A, center, fwhm, sigma))
#
# Guess for  A, center, fwhm from the y_noise!
#
A = np.max(y_noise) - np.min(y_noise)
center = np.mean(x)
sigma = np.sqrt(np.abs(np.sum(
    (x-(np.sum(x*y_noise)/np.sum(y_noise)))**2 * y_noise)/np.sum(y_noise)))
fwhm = sigma * np.sqrt(8*np.log(2))
print("Using guess:   A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    A, center, fwhm, sigma))

#
# Fitting
#
init_values = [A, center, fwhm]     # for [amp, cen, wid]
coefficients, _ = curve_fit(gaussian, x, y_noise, p0=init_values)
sigma = coefficients[2] / np.sqrt(8*np.log(2))
print("Fitted Coeffs: A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    coefficients[0], coefficients[1], coefficients[2], sigma))

y_fit = gaussian(x, *coefficients)

plt.figure()
plt.plot(x, y, '-', label="Perfect")
# plt.plot(x, y_noise, '.', label="noise")
plt.errorbar(x, y_noise, yerr=y_error, fmt='o', capthick=2, label="Noisy")
plt.plot(x, y_fit, '-', label="Fit")
plt.legend()
plt.show()
