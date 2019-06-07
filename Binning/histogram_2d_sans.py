import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Generate a sans detector
x = np.linspace(0.01, 1, 192)
y = np.linspace(0.01, 1, 256)
xx, yy = np.meshgrid(x, y, sparse=False)
z = np.sqrt(xx**2 + yy**2)

# plt.figure()
# plt.pcolor(x,y,z)
# plt.colorbar()


counts, xedges, yedges = np.histogram2d(
    xx.ravel(), yy.ravel(),
    #bins = [x, y],
    #bins = [20, 26],
    bins = 10,
    weights=z.ravel())


# Calculate the bin centers
# xcenters = (xedges[:-1] + xedges[1:]) / 2
# ycenters = (yedges[:-1] + yedges[1:]) / 2

# Print using an image:
# plt.figure()
# plt.imshow(counts.T, interpolation='nearest', origin='low',
#         extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
# plt.colorbar()

plt.figure()
X, Y = np.meshgrid(xedges, yedges)
plt.pcolormesh(X, Y, counts.T)

plt.show()
