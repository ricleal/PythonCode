#!/usr/bin/env python3
import sys

import matplotlib.pyplot as plt
from matplotlib import colors
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


def angle_calculation(data_x, data_y, data_z):
    angle = np.arctan2(data_y, data_x)
    return data_x, data_y, angle


def wedge_calculation(data_x, data_y, data_z, angle, phi_0=0, phi_apperture=30):
    '''

    '''
    # Let's work in radians
    phi_0 = np.deg2rad(phi_0)
    phi_apperture = np.deg2rad(phi_apperture)

    phi_apperture_min = phi_0 - phi_apperture/2
    phi_apperture_max = phi_0 + phi_apperture/2
    # oposite 180 degrees apart
    phi_apperture_min_pi = phi_apperture_min + np.pi
    phi_apperture_max_pi = phi_apperture_max + np.pi
    # if phi_apperture_max_pi > np.pi:
    #     phi_apperture_max_pi = - phi_apperture_max_pi % np.pi

    print("Apertures:", phi_apperture_min, phi_apperture_max,
          phi_apperture_min_pi, phi_apperture_max_pi)
    print("Angles", angle.min(), angle.max())
    print("data_y", data_y.min(), data_y.max())

    condition1 = (angle > phi_apperture_min) & (angle < phi_apperture_max)
    # condition = ((angle > phi_apperture_min) & (angle < phi_apperture_max)) \
    #     | ((angle > phi_apperture_min_pi) & (angle < phi_apperture_max_pi))

    # make angle > np.pi varying between np.pi and 2*np.pi
    angle[angle < 0] = 2*np.pi + angle[angle < 0] 
    condition2 = (angle > phi_apperture_min_pi) & (angle < phi_apperture_max_pi)
    
    condition = condition1 | condition2

    data_x = data_x[condition]
    data_y = data_y[condition]
    data_z = data_z[condition]
    return data_x, data_y, data_z


def wedge_integration(x, y, z, bins=100, statistic='mean'):

    q_bin_centers = np.sqrt(np.square(x) + np.square(y))

    intensity_statistic, q_bin_edges, q_binnumber = stats.binned_statistic(
        q_bin_centers, z, statistic=statistic, bins=bins)
    
    q_bin_centers = (q_bin_edges[1:] + q_bin_edges[:-1]) / 2.0

    return q_bin_centers, intensity_statistic


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

    xedges_width = (xedges[1] - xedges[0])
    xedges_center = xedges[1:] - xedges_width / 2

    yedges_width = (yedges[1] - yedges[0])
    yedges_center = yedges[1:] - yedges_width / 2

    return H, xedges_center, yedges_center


def do_the_job(file_name):
    qx, qy, i, _ = get_data(file_name)

    # QxQy: 1D -> 2D
    shape_qx = len(np.unique(qx))
    shape_qy = len(np.unique(qy))
    qx_2d = qx.reshape(shape_qx, shape_qy)
    qy_2d = qy.reshape(shape_qx, shape_qy)
    i_2d = i.reshape(shape_qx, shape_qy)

    # Plot QxQy
    fig = plt.figure()
    ax1 = fig.add_subplot(321)
    im = ax1.pcolor(qx_2d, qy_2d, i_2d,
                    norm=colors.LogNorm(vmin=1e-3, vmax=i_2d.max()))  # log
    plt.colorbar(im, ax=ax1)
    ax1.set_ylabel('Qy')
    ax1.set_xlabel('Qx')
    ax1.set_title("QxQy")

    # Sectors
    H, x, y = sector_average(qx, qy, i)
    ax2 = fig.add_subplot(322)
    X, Y = np.meshgrid(x, y)
    #im = ax2.contourf(X, Y, H.T, 150)
    im = ax2.pcolor(X, Y, H.T)
    plt.colorbar(im, ax=ax2)
    ax2.set_ylabel('Sector Averaging')
    ax2.set_xlabel("Angle")
    ax2.set_ylabel("Radius")

    # Angle
    ax3 = fig.add_subplot(323)
    x, y, angle = angle_calculation(qx, qy, i)
    im3 = ax3.scatter(x, y, c=angle, s=50, edgecolor='', marker='s')
    plt.colorbar(im3, ax=ax3)
    ax3.set_ylabel('Angle')
    ax3.set_xlabel("Qx")
    ax3.set_ylabel("Qy")

    # Wedge
    ax4 = fig.add_subplot(324)
    x, y, z = wedge_calculation(qx, qy, i, angle, phi_0=30, phi_apperture=45)
    im = ax4.scatter(x, y, c=z, s=50, edgecolor='', marker='s')
    plt.colorbar(im, ax=ax4)
    ax4.set_ylabel('Wedge')
    ax4.set_xlabel("Qx")
    ax4.set_ylabel("Qy")

    # Wedge integration
    ax5 = fig.add_subplot(325)
    x1d, y1d = wedge_integration(x, y, z)
    ax5.plot(x1d, y1d)
    ax5.set_ylabel('Wedge Integration')
    ax5.set_xlabel("Q")
    ax5.set_ylabel("I(q)")
    

    plt.show()
    # plt.show(block=False)
    # plt.pause(3)
    # plt.close()


def main():
    if len(sys.argv) != 2:
        print("Usage " + sys.argv[0] + " Iqxy.dat file")
    else:
        do_the_job(sys.argv[1])


if __name__ == "__main__":
    main()
