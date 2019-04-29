import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# normal distribution centred in 0, std=0.03
noise = np.random.normal(0, 0.03, 500)

# Coordinates (x,y) of a circle
t = np.linspace(-np.pi, np.pi, 500)
x = np.sin(t) + noise
y = np.cos(t) + noise


x_axis = np.linspace(x.min()-0.1, x.max()+0.1, 20)
y_axis = np.linspace(y.min()-0.1, y.max()+0.1, 20)

# counts it's 2D
#  xedges, yedges are the same as x_axis, y_axis
counts, xedges, yedges = np.histogram2d(x, y, bins=[x_axis, y_axis])

print(x_axis.shape, y_axis.shape, counts.shape)
plt.figure()
plt.pcolormesh(x_axis, y_axis, counts)
plt.plot(x, y, 'r.')
plt.colorbar()
plt.show()
