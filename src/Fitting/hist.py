# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:57:33 2015

@author: rhf
"""

from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np

# Random normal distribution
data_mu, data_sigma = 0, 0.1 # mean and standard deviation
data = np.random.normal(data_mu, data_sigma, 10000)

# best fit of data
(mu, sigma) = norm.fit(data)

# the histogram of the data
n, bins, patches = plt.hist(data, 50, normed=True,
                            facecolor='yellow', alpha=0.5)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'b-')

#plot
plt.xlabel('Whatever you want...')
plt.ylabel('Probability')
plt.title(r'$\mu_{orig}=%.3f,\ \sigma_{orig}=%.3f$      $\mu_{fit}=%.3f,\ \sigma_{fit}=%.3f$' %(data_mu, data_sigma, mu, sigma))
plt.grid(True)

plt.show()