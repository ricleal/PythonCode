import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

tranlation = 240 #in mm

def twoD_Gaussian((x, y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2) / (2 * sigma_x**2) + \
        (np.sin(theta)**2) / (2 * sigma_y**2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x**2) + \
        (np.sin(2 * theta)) / (4 * sigma_y**2)
    c = (np.sin(theta)**2) / (2 * sigma_x**2) + \
        (np.cos(theta)**2) / (2 * sigma_y**2)
    g = offset + amplitude * np.exp(- (a * ((x - xo)**2) + 2 * b * (x - xo) * (y - yo)
                                       + c * ((y - yo)**2)))
    return g.ravel()

def create_2d_array(x_dim=192, y_dim=256):
    """
    Generate some 2d gaussian data
    """
    # Create x and y indices
    x = np.linspace(0, 200, x_dim)
    y = np.linspace(0, 200, y_dim)
    x, y = np.meshgrid(x, y)
    data = twoD_Gaussian((x, y), 5, 50, 100, 20, 20, 0, 0)
    data_2d = data.reshape(y_dim,x_dim)
    return data_2d

def get_axes_units(data_shape, pixel_size=[4,5]):
    """
    pixel_size in mm
    get default units with center as center of the images
    """
    i_center = data_shape[1]/2
    j_center = data_shape[0]/2
    x_axis_units = (np.arange(data_shape[1])-i_center) * pixel_size[1]
    y_axis_units = (np.arange(data_shape[0])-j_center) * pixel_size[0]
    return x_axis_units, y_axis_units


data_2d = create_2d_array()
x_units_centred,y_units_centred = get_axes_units(data_2d.shape, pixel_size=[4,5])
# Let's center real cooedinates at the translation
x_units_centred += tranlation

#
# Noise
#
poisson_noise = np.random.poisson(0.5,data_2d.shape).astype(float)
data_2d_noisy = data_2d + poisson_noise

#
#
#

def detect_peaks(image):
    """
    Takes an image and detect the peaks usingthe local maximum filter.
    Returns a boolean mask of the peaks (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """

    # define an 8-connected neighborhood
    neighborhood = generate_binary_structure(2,2)

    #apply the local maximum filter; all pixel of maximal value
    #in their neighborhood are set to 1
    local_max = maximum_filter(image, footprint=neighborhood)==image
    #local_max is a mask that contains the peaks we are
    #looking for, but also the background.
    #In order to isolate the peaks we must remove the background from the mask.

    #we create the mask of the background
    background = (image==0)

    #a little technicality: we must erode the background in order to
    #successfully subtract it form local_max, otherwise a line will
    #appear along the background border (artifact of the local maximum filter)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    #we obtain the final mask, containing only peaks,
    #by removing the background from the local_max mask
    detected_peaks = local_max - eroded_background

    return detected_peaks

#
# Plotting
#
X = x_units_centred
Y = y_units_centred
Z = data_2d_noisy
plt.figure("Default Units")
plt.imshow(Z, extent = (X[0], X[-1], Y[0], Y[-1]))
plt.contour(X, Y, Z,10)
# Let's put a Marker at [0,0]
#plt.scatter(,marker='+', color="white", s=50)

peak = detect_peaks(data_2d)
plt.figure("peak")
plt.imshow(peak)


plt.show()
