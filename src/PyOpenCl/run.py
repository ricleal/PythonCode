#!/usr/bin/env python

'''
Created on Oct 10, 2014

@author: rhf

Based on : https://github.com/HMP1/Cylinder

'''


from cylinder import *
import mpl_toolkits.mplot3d.axes3d as p3
from time import time
import matplotlib.pyplot as plt
    
def demo():
    

    #create qx and qy evenly spaces (128 points)
    qx = np.linspace(-.02, .02, 128)
    qy = np.linspace(-.02, .02, 128)
    print qx.shape, qy.shape
    qx, qy = np.meshgrid(qx, qy)
    print qx.shape, qy.shape
    
    #saved shape of qx
    r_shape = qx.shape

    #reshape for calculation; resize as float32
    qx = qx.flatten()
    qy = qy.flatten()
    print qx.shape, qy.shape
    
    pars = CylinderParameters(scale=1,
                              radius=64.1,
                              length=266.96, 
                              sldCyl=.291e-6, 
                              sldSolv=5.77e-6, 
                              background=0,
                              cyl_theta=0, 
                              cyl_phi=0, 
                              M0_sld_cyl=1.0e-33, 
                              M0_sld_solv=1.0e-33)
    
    print "Starting GPU Processing..."
    t = time()
    result = GpuCylinder(qx, qy)
    result.x = result.cylinder_fit(qx, qy, pars, r_n=10, t_n=10, l_n=10, p_n=10, sigma=3, r_w=.1, t_w=.1, l_w=.1, p_w=.1)
    result.x = np.reshape(result.x, r_shape)
    tt = time()

    print("Time taken: %f" % (tt - t))

    
    plt.pcolormesh(result.x)
    #plt.imshow(result.x)
    plt.show()

if __name__=="__main__":
    print "Starting..."
    demo()
    print "End!"



