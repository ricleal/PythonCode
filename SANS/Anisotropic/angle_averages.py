#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import math
import scipy.stats as stats
from pylab import figure, cm
import sys
from matplotlib.colors import LogNorm
from scipy.optimize import leastsq
from scipy import signal
from scipy import interpolate
from scipy import stats
from scipy.interpolate import UnivariateSpline

'''
find . -iname "*.dat" -exec  python angle_averages.py {} \;
'''

def get_data(file_name):
    '''
    No reshape in 2d
    '''
    data = np.genfromtxt(file_name, dtype=float, delimiter=None,
                         skip_header=2, names=["Qx", "Qy", "I(Qx,Qy)", "err(I)"])
    shape_x = len(np.unique(data['Qx']))
    shape_y = len(np.unique(data['Qy']))
    data_x = data['Qx']#.reshape(shape_x, shape_y)
    data_y = data['Qy']#.reshape(shape_x, shape_y)
    data_z = data['IQxQy']#.reshape(shape_x, shape_y)
    return data_x, data_y, data_z

def radial_average(data_x, data_y, data_z):
    '''

    '''
    angle = np.arctan2(data_y, data_x)
    angle = np.rad2deg(angle)
    # make it integer from 0 to 360
    angle = np.round(angle).astype(int) + 180

    # limit Q range
    q = np.linalg.norm(np.column_stack((data_x, data_y)), axis=1)
    q_condition = q<0.35

    angle_and_intensity_sum = np.bincount(angle[q_condition],
        weights=data_z[q_condition])
    angle_and_intensity_counts = np.bincount(angle[q_condition])

    angle_and_intensity_average = angle_and_intensity_sum / angle_and_intensity_counts.astype(np.float64)
    angle_and_intensity_average = np.nan_to_num(angle_and_intensity_average) # because division by 0
    angle_and_intensity_average = np.tile(angle_and_intensity_average, 2) # duplicates array

    return angle_and_intensity_average[:450]

def do_the_job(file_name):
    data_x, data_y, data_z = get_data(file_name)
    shape_x = len(np.unique(data_x))
    shape_y = len(np.unique(data_y))
    X = data_x.reshape(shape_x, shape_y)
    Y = data_y.reshape(shape_x, shape_y)
    Z = data_z.reshape(shape_x, shape_y)

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(121)
    ax1.pcolormesh(X,Y,Z)
    #ax1.pcolor(X, Y, Z, norm=LogNorm())

    angle_and_intensity_average = radial_average(data_x, data_y, data_z)

    # normalize to 1
    angle_and_intensity_average = (angle_and_intensity_average - angle_and_intensity_average.min()) / (angle_and_intensity_average.max() - angle_and_intensity_average.min())

    x = np.arange(450)

    ax2 = fig.add_subplot(122)
    ax2.plot(x,angle_and_intensity_average,'b.',label="raw")

    # histogram
    # the histogram of the data
    # Integration
    n_bins = 50
    bin_means, bin_edges, binnumber = stats.binned_statistic(x, angle_and_intensity_average, statistic='sum', bins=n_bins)
    bin_width = (bin_edges[1] - bin_edges[0])
    bin_centers = bin_edges[1:] - bin_width/2
    # normalize to 1
    bin_means = (bin_means - bin_means.min()) / (bin_means.max() - bin_means.min())
    ax2.plot(bin_centers,bin_means,'r', label="binning")

    # Spline interpolation
    spl = UnivariateSpline(bin_centers, bin_means)
    spl.set_smoothing_factor(0.5)
    xs = np.linspace(bin_centers.min(), bin_centers.max(), 1000)
    ax2.plot(xs, spl(xs), 'g',label="spline")
    ax2.legend()

    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage " + sys.argv[0]+ " Iqxy.dat file")
    else:
        do_the_job(sys.argv[1])

if __name__ == "__main__":
    main()
