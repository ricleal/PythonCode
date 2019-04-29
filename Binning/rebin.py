import numpy as np
import matplotlib.pyplot as plt
import cv2

## Generate a sans detector
x = np.linspace(0.01, 1, 192)
y = np.linspace(0.01, 1, 256)
xx, yy = np.meshgrid(x, y, sparse=False)
z = np.sqrt(xx**2 + yy**2)

plt.figure()
plt.pcolor(x,y,z)
plt.colorbar()


# Rebin
X_SIZE, Y_SIZE = (30, 30)
res = cv2.resize(z, dsize=(X_SIZE, Y_SIZE), interpolation=cv2.INTER_LINEAR)
qx = np.linspace(0.01, 0.8, X_SIZE)
qy = np.linspace(0.01, 0.9, Y_SIZE)

# Log binning
qx_log = np.logspace(np.log10(qx.min()), np.log10(qx.max()), len(qx), base=10)
qy_log = np.logspace(np.log10(qy.min()), np.log10(qy.max()), len(qy), base=10)

# Plot
plt.figure()
plt.pcolormesh(qx_log, qy_log, res)
plt.colorbar()
plt.show()
