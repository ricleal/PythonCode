import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import math
import scipy.stats as stats
from pylab import figure, cm
import sys
from matplotlib.colors import LogNorm
from scipy.optimize import leastsq

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

    angle_and_intensity_average = angle_and_intensity_sum / angle_and_intensity_counts
    angle_and_intensity_average = np.tile(angle_and_intensity_average, 2) # duplicates array

    return angle_and_intensity_average[:450]



######################################
# Setting up test data
def norm(x, mean, sd, b):
  norm = []
  for i in range(x.size):
    norm += [ (1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))) + b]
  return np.array(norm)

######################################

def res(p, y, x):
  m, dm, sd1, sd2,b = p
  m1 = m
  m2 = m1 + dm
  y_fit = norm(x, m1, sd1, b) + norm(x, m2, sd2, b)
  err = y - y_fit
  return err


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
    x = np.arange(450)
    # Solving
    m, dm, sd1, sd2, b = [180, 260, 1, 1, 0.1]
    p = [m, dm, sd1, sd2, b] # Initial guesses for leastsq
    plsq = leastsq(res, p, args = (angle_and_intensity_average, x))
    y_est = norm(x, plsq[0][0], plsq[0][2], plsq[0][4]) + norm(x, plsq[0][0] + plsq[0][1], plsq[0][3], plsq[0][4])

    ax2 = fig.add_subplot(122)
    ax2.plot(x,angle_and_intensity_average)
    ax2.plot(x, y_est, 'g.')

    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage " + sys.argv[0]+ " Iqxy.dat file")
    else:
        do_the_job(sys.argv[1])

if __name__ == "__main__":
    main()
