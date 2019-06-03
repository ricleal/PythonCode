#!/usr/bin/env python3
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


'''
find . -iname "*.dat" -exec  python angle_averages.py {} \;
'''


def get_data(file_name):
    '''
    No reshape in 2d
    '''
    data = np.genfromtxt(file_name, delimiter=None, skip_header=2,
                         names=["Qx", "Qy", "I(Qx,Qy)", "err(I)"])
    qx = data['Qx']
    qy = data['Qy']
    i = data['IQxQy']
    err_i = data['IQxQy']
    return qx, qy, i, err_i


def wedge_integration(data_x, data_y, data_z, phi_0=0, phi_apperture=30,
                      bins=100, statistic='mean'):
    '''

    '''
    
    angle = np.arctan2(data_y, data_x)


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
    #data_z = (data_z - data_z.min()) / (data_z.max() - data_z.min())

    H, xedges, yedges, binnumber = stats.binned_statistic_2d(
        angle, radius, data_z, bins=[
            n_bins_angle, n_bins_radius], statistic='mean')

    print(H.shape)
    xedges_width = (xedges[1] - xedges[0])
    xedges_center = xedges[1:] - xedges_width / 2

    yedges_width = (yedges[1] - yedges[0])
    yedges_center = yedges[1:] - yedges_width / 2

    return H, xedges_center, yedges_center


def do_the_job(file_name):
    qx, qy, i, _ = get_data(file_name)

    # QxQy
    shape_qx = len(np.unique(qx))
    shape_qy = len(np.unique(qy))

    qx_2d = qx.reshape(shape_qx, shape_qy)
    qy_2d = qy.reshape(shape_qx, shape_qy)
    i_2d = i.reshape(shape_qx, shape_qy)

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.pcolor(qx_2d, qy_2d, i_2d)
    ax1.set_ylabel('Qy')
    ax1.set_xlabel('Qx')
    ax1.set_title("QxQy")

    # Sectors
    H, x, y = sector_average(qx, qy, i)
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
