# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 17:30:06 2014

@author: rhf

- Gaussian distribution
- histogram
- fit of the histogram
- smooth of the plot

"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.interpolate import spline

# Define some test data which is close to Gaussian
data = np.random.normal(loc=0.0, scale=1.0, size=10000)

hist, bin_edges = np.histogram(data,bins=25, density=True)
bin_centres = (bin_edges[:-1] + bin_edges[1:])/2

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

# p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
p0 = [1., 0., 1.]

coeff, var_matrix = curve_fit(gauss, bin_centres, hist, p0=p0)

# Get the fitted curve
hist_fit = gauss(bin_centres, *coeff)

plt.plot(bin_centres, hist,'bo', label='Test data')
plt.plot(bin_centres, hist_fit,'rx', label='Fitted data')

# smooth
xnew = np.linspace(bin_centres[0],bin_centres[-1],200)
hist_smooth = spline(bin_centres,hist_fit,xnew)
plt.plot(xnew,hist_smooth,'r-')

# Finally, lets get the fitting parameters, i.e. the mean and standard deviation:
print 'Fitted mean = ', coeff[1]
print 'Fitted standard deviation = ', coeff[2]

plt.show()

