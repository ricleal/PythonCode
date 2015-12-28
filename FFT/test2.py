import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, fftpack



I = plt.imread('pattern.jpg')

# FFT
# F = np.fft.fft2(I)
# im = np.log(np.abs(np.fft.fftshift(F))**2)
# plt.imshow(im, cmap='gray')
# IFFT
IF = np.fft.ifft2(I)
im = np.log(np.abs(IF)**2)
plt.imshow(im, cmap='gray')

plt.colorbar()
plt.show()
# 2**10
# I = np.arange(1, n)
# x = I - n / 2
# y = n / 2 - I
# 
# R = 10
# 
# X = x[:, np.newaxis]
# Y = y[np.newaxis, :]
# 
# M = X**2 + Y**2 < R**2
# 
# plt.imshow(M)
# plt.show()
# 
# D1 = fftpack.fft2(M)
# D2 = fftpack.fftshift(D1)
# 
# abs_image = np.abs(D2)
# plt.imshow(abs_image)
# plt.show()