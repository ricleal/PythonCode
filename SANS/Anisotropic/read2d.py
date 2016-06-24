#!/usr/bin/env python

from __future__ import print_function, division  # We require Python 2.6 or later

import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.colors import LogNorm

def parse_and_plot_qxqy_file(file_name):
    data = np.genfromtxt(file_name, dtype=float, delimiter=None,
                         skip_header=2, names=["Qx", "Qy", "I(Qx,Qy)", "err(I)"])
    shape_x = len(np.unique(data['Qx']))
    shape_y = len(np.unique(data['Qy']))
    X = data['Qx'].reshape(shape_x, shape_y)
    Y = data['Qy'].reshape(shape_x, shape_y)
    Z = data['IQxQy'].reshape(shape_x, shape_y)

    plt.pcolormesh(X,Y,Z)
    #plt.pcolor(X, Y, Z, norm=LogNorm(vmin=0, vmax=Z.max()), cmap='PuBu_r')
    plt.colorbar()

    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage " + sys.argv[0]+ " Iqxy.dat file")
    else:
        parse_and_plot_qxqy_file(sys.argv[1])

if __name__ == "__main__":
    main()
