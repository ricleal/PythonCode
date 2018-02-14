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
A = 5
center = 5
fwhm = 2

x = np.linspace(0, 10, 50)
y = lorentzian(x, A, center, fwhm)
# Add random noise to the data
y_noise = y + np.random.normal(0, 0.3, len(y))
y_error = np.sqrt(np.abs(y_noise))

sigma = fwhm / 2
print("Ideal:         A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    A, center, fwhm, sigma))
#
# Guess for  A, center, fwhm from the y_noise!
#
A = np.max(y_noise) - np.min(y_noise)
center = np.sum(x*y_noise)/np.sum(y_noise)
sigma = np.sqrt(np.abs(
    np.sum((x-center)**2 * y_noise)/np.sum(y_noise)
))

fwhm = 2 * sigma
print("Using guess:   A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    A, center, fwhm, sigma))

#
# Fitting
#
init_values = [A, center, fwhm]     # for [amp, cen, wid]
coefficients, _ = curve_fit(lorentzian, x, y_noise, p0=init_values)
sigma = coefficients[2] / 2
print("Fitted Coeffs: A={:.2f} center={:.2f} fwhm={:.2f} (sigma={:.2f}).".format(
    coefficients[0], coefficients[1], coefficients[2], sigma))

y_fit = lorentzian(x, *coefficients)

plt.figure()
plt.plot(x, y, '-', label="Perfect")
# plt.plot(x, y_noise, '.', label="noise")
plt.plot(x, lorentzian(x, A, center, fwhm), '-', label="Guess")
plt.errorbar(x, y_noise, yerr=y_error, fmt='.', label="Noisy")
plt.plot(x, y_fit, '-', label="Fit")
plt.legend()
plt.show()
