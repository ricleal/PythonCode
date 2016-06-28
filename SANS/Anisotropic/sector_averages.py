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
from scipy.optimize import curve_fit

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
    data_x = data['Qx']  # .reshape(shape_x, shape_y)
    data_y = data['Qy']  # .reshape(shape_x, shape_y)
    data_z = data['IQxQy']  # .reshape(shape_x, shape_y)
    return data_x, data_y, data_z

def sector_average(data_x, data_y, data_z, n_bins_angle=100, n_bins_radius=50):
    '''

    '''
    angle = np.arctan2(data_y, data_x)
    angle = np.rad2deg(angle)
    # make it integer from 0 to 360
    angle = np.round(angle).astype(int) + 180
    
    # radius for every pixel
    radius = np.linalg.norm(np.column_stack((data_x, data_y)), axis=1)
    
    # normalize data to 1
    data_z = (data_z - data_z.min()) / (data_z.max() - data_z.min())
        
    H, xedges, yedges, binnumber = stats.binned_statistic_2d(angle, radius, data_z,
                                       bins=[n_bins_angle, n_bins_radius], 
                                       statistic='mean')
    
    xedges_width = (xedges[1] - xedges[0])
    xedges_center = xedges[1:] - xedges_width / 2
    
    yedges_width = (yedges[1] - yedges[0])
    yedges_center = yedges[1:] - yedges_width / 2
    
    return H, xedges_center, yedges_center


def do_the_job(file_name):
    data_x, data_y, data_z = get_data(file_name)
    
    # Raw image
    shape_x = len(np.unique(data_x))
    shape_y = len(np.unique(data_y))
    X = data_x.reshape(shape_x, shape_y)
    Y = data_y.reshape(shape_x, shape_y)
    Z = data_z.reshape(shape_x, shape_y)

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(121)
    ax1.pcolormesh(X, Y, Z)
  
    # Sectors
    H, x, y = sector_average(data_x, data_y, data_z)
    ax2 = fig.add_subplot(122)
    X, Y = np.meshgrid(x, y)
    ax2.contourf(X, Y, H.T, 150)
    ax2.set_xlabel("Angle")  
    ax2.set_ylabel("Radius")
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage " + sys.argv[0] + " Iqxy.dat file")
    else:
        do_the_job(sys.argv[1])

if __name__ == "__main__":
    main()
