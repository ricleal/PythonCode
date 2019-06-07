import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# 1D arrays
x = np.loadtxt("/SNS/users/rhf/Desktop/x.txt")
y = np.loadtxt("/SNS/users/rhf/Desktop/y.txt")
z = np.loadtxt("/SNS/users/rhf/Desktop/z.txt")

print("****", len(x), len(y))

def twoD_Gaussian( (x, y) , amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)    
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)))
    return g.ravel()

dim_x = len(x)
dim_y = len(y)

# Let's pad x (y and x must be have the same dims)
pad = int((dim_y - dim_x) / 2)
x = np.pad(x, (pad, pad), 'reflect', reflect_type='odd')
print("**** After Padding", len(x), len(y))

xx, yy = np.meshgrid(x, y)

data = z.reshape(dim_x, dim_y)
data = data.T
data = np.log(data)

data[data == np.inf] = 0
data[data == -np.inf] = 0
data = np.nan_to_num(data)

data = np.pad(data, [(0,0),(pad, pad)], mode='constant', constant_values=0)
print('*** Shapes',   xx.shape, yy.shape, data.shape)



## 
initial_guess = (12, 0, 0, 2, 2, 0, 0)

popt, pcov = opt.curve_fit(twoD_Gaussian, (xx, yy), data.flatten(), p0=initial_guess)

data_fitted = twoD_Gaussian((xx, yy), *popt)

fig, ax = plt.subplots(1, 1)
ax.imshow(data, origin='bottom',
    extent=(x.min(), x.max(), y.min(), y.max()))
ax.contour(xx, yy, data_fitted.reshape(data.shape), 8, colors='w')
plt.show()