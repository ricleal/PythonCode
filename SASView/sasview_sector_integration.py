from __future__ import print_function

import sys
import os
import argparse
import platform

import numpy as np
from matplotlib import pyplot as plt

#
# Sasview imports
#

# Git clone built from source

if platform.system() == 'Linux' and platform.linux_distribution()[0] == 'Red Hat Enterprise Linux Workstation':
    # Analysis
    sasview_directory = '/usr/lib/python2.7/site-packages/sasview-4.1-py2.7-linux-x86_64.egg'
elif platform.system() == 'Linux':
    sasview_directory = '/home/rhf/git/sasview/build/lib.linux-x86_64-2.7'
else:
    sasview_directory = '/Users/rhf/git/sasview/build/lib.macosx-10.11-x86_64-2.7'

# OSx Binary Installation
# Old version apparently: The `SectorQ` function has no `base` option
# sasview_directory = '/Applications/SasView 4.1.2.app/Contents/Resources/lib/python2.7/site-packages.zip'

sys.path.append(sasview_directory)
from sas.sascalc.dataloader.readers.red2d_reader import Reader
from sas.sascalc.dataloader.manipulations import Sectorcut, SectorQ


'''
This must run with python 2!

Example:

# Feature Wedge
python2 sasview_sector_integration.py Data/Venky3/BioSANS_exp322_scan0024_0001_m_Iqxy.dat 8 36
#  Non Feature
python2 sasview_sector_integration.py Data/Venky3/BioSANS_exp322_scan0024_0001_m_Iqxy.dat 90 36


'''

def parse_arguments():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Reduced QxQy file")
    parser.add_argument("phi_center", type=float, help="Phi Center in degrees")
    parser.add_argument("phi_width", type=float, help="Phi Width in degrees")
    args = parser.parse_args()
    return args

def plot_iqxqy(data):
    '''
    @param data :: Output of Sasview Reader
    '''
    qx = data.qx_data
    qy = data.qy_data
    iqxqy = data.data
    # Reshape the data as 2D
    plt.figure()
    plt.scatter(qx, qy, c=np.log(iqxqy), s=50, edgecolor='', marker='s')
    plt.colorbar()
    # plt.show()

def plot_iq(data):
    '''
    @param data :: is 1D
    '''
    # Plot in 1D log scale
    plt.figure()
    plt.yscale('log', nonposy='clip')
    plt.xscale('log', nonposx='clip')
    plt.errorbar(data.x, data.y, yerr=data.dy)


def integrate_wedge(data, phi_center, phi_width, nbins=100):
    '''
    @param base: must be a valid base for an algorithm, i.e., a positive number
    The code for integration is here:
    https://github.com/SasView/sasview/blob/master/src/sas/sascalc/dataloader/manipulations.py
    '''
    phi_min = phi_center - phi_width/2.0
    phi_max = phi_center + phi_width/2.0

    print("Integrating from {} to {}".format(phi_min, phi_max))

    phi_min = np.deg2rad(phi_min)
    phi_max = np.deg2rad(phi_max)
    
    sector_wedge = SectorQ(r_min=0.0001, r_max=1, phi_min=phi_min, 
                           phi_max=phi_max, nbins=nbins)
    iq_wedge = sector_wedge(data)
    return iq_wedge


def main():
    args = parse_arguments()
    r = Reader()
    data = r.read(args.filename)
    if type(data) == list:
        data = data[0]
    plot_iqxqy(data)
    iq_wedge = integrate_wedge(data, args.phi_center, args.phi_width, nbins=50)
    plot_iq(iq_wedge)
    plt.show()


if __name__ == "__main__":
    main()

