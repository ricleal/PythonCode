import numpy as np
import matplotlib.pyplot as plt

'''

TODO: INCOMPLETE!!!

'''

class Binning2D(object):
    '''
    This class just creates a binning object
    either linear or log
    See tests for usage
    '''

    def __init__(self,
                 x_min_value, x_max_value, x_n_bins,
                 y_min_value, y_max_value, y_n_bins,
                 x_base=None, y_base=None):
        '''
        if base is None: Linear binning
        '''
        self.x_min = x_min_value
        self.x_max = x_max_value
        self.x_n_bins = x_n_bins
        self.y_min = y_min_value
        self.y_max = y_max_value
        self.y_n_bins = y_n_bins
        self.x_base = x_base
        self.y_base = y_base
        self.bins = self._compute_binning()

    def _compute_binning(self):
        '''
        '''
        if self.base is None:
            return (
                np.linspace(self.x_min, self.x_max, self.x_n_bins),
                np.linspace(self.y_min, self.y_max, self.y_n_bins)
            )
        else:
            return (
                np.logspace(np.log10(self.x_min), np.log10(self.x_max),
                            self.x_n_bins, base=self.base),
                np.logspace(np.log10(self.y_min), np.log10(self.y_max),
                            self.y_n_bins, base=self.base)
            )

    def _get_bin_index(self, value):
        '''
        value it's a (x,y) tuple
        '''
        assert isinstance(value) == tuple and len(value) == 2

        indices = (
            np.digitize(np.array(value[0]), self.bins[0]),
            np.digitize(np.array(value[1]), self.bins[1])
        )
        return indices

    def get_rebinned_weights(self, x_original_binning, y_original_binning, counts):

        assert len(x_original_binning) == len(y_original_binning)
        assert len(x_original_binning) * len(y_original_binning) == len(counts)

        ret = np.zeros((self.bins[0].shape[0], self.bins[1].shape[0]))
        for x in x_original_binning:
            for y in y_original_binning:
                new_bin_index = self._get_bin_index((x, y))
                ret[new_bin_index[0]][new_bin_index[1]] += counts[x][y]
        return ret


# Generate a sans detector
x = np.linspace(0.01, 1, 192)
y = np.linspace(0.01, 1, 256)
xx, yy = np.meshgrid(x, y, sparse=False)
z = np.sqrt(xx**2 + yy**2)

plt.figure()
plt.pcolor(x, y, z)
plt.colorbar()


# Rebin
X_SIZE, Y_SIZE = (30, 30)
qx = np.linspace(0.01, 0.8, X_SIZE)
qy = np.linspace(0.01, 0.9, Y_SIZE)

# Log binning
qx_log = np.logspace(np.log10(qx.min()), np.log10(qx.max()), len(qx), base=10)
qy_log = np.logspace(np.log10(qy.min()), np.log10(qy.max()), len(qy), base=10)


b = Binning2D(qx_log[0], qx_log[-1], len(qx_log))

counts, xedges, yedges = np.histogram2d(
    xx.ravel(), yy.ravel(),
    bins=[x, y],
    #bins = [20, 26],
    #bins = 10,
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
