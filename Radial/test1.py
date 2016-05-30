import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
Sort of radial integration (average)
'''

# Detector dimensions in pixels
dim_x = 256
dim_y = 256

# Detector distance
Z = 5 #5 meters
# Vector with Z values
z = np.full((dim_x*dim_y), Z)

# Generate data in the detector
xx_pixels, yy_pixels = np.mgrid[0:dim_x, 0:dim_y]
dist = np.hypot(xx_pixels, yy_pixels) # Linear distance from point 0, 0
values = np.square(5*np.cos( dist /200.0 ))
plt.figure()
plt.imshow(values)

# Real coordinates in space. Assuming detector to be squared 1.0x1.0 meters
x_coords = np.linspace(0.0, 1.0, dim_x)
y_coords = np.linspace(0.0, 1.0, dim_y)
xx_coords, yy_coords = np.meshgrid(x_coords, y_coords)

# Let's calulate theta: angle between Z vector [0,0,Z] and the vector from [0,0,0] to every detector pixel [x,y,Z]
v = np.stack((xx_coords.flatten(),yy_coords.flatten(), z), axis=-1)
u = np.stack((np.zeros(dim_x*dim_y),np.zeros(dim_x*dim_y), z), axis=-1)
theta = np.arccos(np.sum(u*v, axis=1)/(np.linalg.norm(u,axis=1) * np.linalg.norm(v,axis=1)))

# Raw data:
plt.figure()
plt.plot(theta,values.flatten(),'.')

# Integration
n_bins = 100
bin_means, bin_edges, binnumber = stats.binned_statistic(theta, values.flatten(), statistic='mean', bins=n_bins)
bin_width = (bin_edges[1] - bin_edges[0])
bin_centers = bin_edges[1:] - bin_width/2
plt.figure()
plt.plot(bin_centers,bin_means)


plt.show()
