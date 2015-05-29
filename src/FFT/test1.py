import matplotlib.pyplot as plt
import numpy as np

[X, Y] = np.meshgrid(4 * np.pi * np.arange(200)/10 ,
                      4 * np.pi * np.arange(200)/10 )


mu, sigma = 0, 0.01 # mean and standard deviation
dist = np.random.normal(mu, sigma, X.shape)
#dist = np.random.uniform(0, 1, X.shape)

S = np.sin(X) + np.cos(Y) + dist

#plt.contour(X, Y, S,10)
plt.imshow(S)
plt.show()

FS = np.fft.ifftn(S)

im = np.log(np.abs(np.fft.fftshift(FS))**2)


plt.imshow(im)
plt.show()
