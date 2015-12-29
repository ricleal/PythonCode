#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''
import numpy as np
import matplotlib.pyplot as plt
from astropy.stats import histogram

mu, sigma = 100, 15
data = mu + sigma * np.random.randn(5000)

#weights = data / data.max()
hist, bin_edges = histogram(data, bins='blocks')

print 'Bin widths:', bin_edges[1:] - bin_edges[:-1]
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
plt.plot(bin_centers, hist,'.')
plt.show()


#if __name__ == '__main__':
