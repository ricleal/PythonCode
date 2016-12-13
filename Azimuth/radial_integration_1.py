import numpy as np
import matplotlib.pyplot as plt

from radialprofile import azimuthalAverage

def convert_to_8bits(image):
    image = np.array(image, copy=True)
    image //= (np.max(image) - np.min(image) + 1) / 256.
    return image.astype(np.uint8)

def radial_profile(data, center):
    y, x = np.indices((data.shape))  # first determine radii of all pixels
    r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    ind = np.argsort(r.flat)  # get sorted indices
    sr = r.flat[ind]  # sorted radii
    sim = data.flat[ind]  # image values sorted by radii
    ri = sr.astype(np.int32)  # integer part of radii (bin size = 1)
    # determining distance between changes
    deltar = ri[1:] - ri[:-1]  # assume all radii represented
    rind = np.where(deltar)[0]  # location of changed radius
    nr = rind[1:] - rind[:-1]  # number in radius bin
    # cumulative sum to figure out sums for each radii bin
    csim = np.cumsum(sim, dtype=np.float64)
    # sum for image values in radius bins
    tbin = csim[rind[1:]] - csim[rind[:-1]]
    radialprofile = tbin / nr  # the answer
    return radialprofile



#img = np.random.randint(0, 255, (100,100))

x, y = np.mgrid[-100:100:200j, -100:100:200j]
dist = np.hypot(x, y) # Linear distance from point 0, 0
img = np.cos( dist/5 / np.pi)
plt.figure()
plt.imshow(img)
plt.colorbar()
plt.show()


img = convert_to_8bits(img)
plt.figure()
plt.imshow(img,cmap="hot")
plt.colorbar()
plt.show()


# center, radi = find_centroid(img)
center, radi = (100, 100), 5
rad = radial_profile(img, center)

plt.figure("Method 1")
plt.plot(rad[radi:])
#plt.show()

# Other method
az = azimuthalAverage(img)
plt.figure("Method 2")
plt.plot(az)
plt.show()
