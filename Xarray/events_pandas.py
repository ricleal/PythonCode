#!/usr/bin/env python

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def cart2sph(x, y, z):
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(z, hxy)
    az = np.arctan2(y, x)
    return az, el, r

def sph2cart(az, el, r):
    rcos_theta = r * np.cos(el)
    x = rcos_theta * np.cos(az)
    y = rcos_theta * np.sin(az)
    z = r * np.sin(el)
    return x, y, z

def plot_scatter_3d(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for x,y,z in data:
        ax.scatter(x,y,z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def generate_initial():
    #detector
    coords = np.array([ sph2cart(az,el,2) for az in np.linspace(0,np.pi) for el in np.linspace(0,np.pi)])
    return coords

data = generate_initial()
plot_scatter_3d(data)
