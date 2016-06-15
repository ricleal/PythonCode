import matplotlib.pyplot as plt
import numpy as np

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


# Not centered Figure
X = x_units_centred
Y = y_units_centred
Z = data_2d
plt.figure("Default Units")
plt.imshow(Z, extent = (X[0], X[-1], Y[0], Y[-1]))
plt.contour(X, Y, Z,10)
# Let's put a Marker at [0,0]
plt.scatter([0],[0],marker='+', color="white", s=50)

# Centered
X= x_units_centred + tranlation
plt.figure("Default Units: CENTERED!")
plt.imshow(Z, extent = (X[0], X[-1], Y[0], Y[-1]))
plt.contour(X, Y, Z,10)
# Let's put a Marker at [0,0]
plt.scatter([0],[0],marker='+', color="white", s=50)

plt.show()
