import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, fftpack

"""
Source : http://stackoverflow.com/questions/20517309/converting-a-matlab-fft2-diffraction-example-into-python

"""
# n = 2**10
# I = np.arange(1, n)
# x = I - n / 2
# y = n / 2 - I

# R = 10

# X = x[:, np.newaxis]
# Y = y[np.newaxis, :]


# M = X**2 + Y**2 < R**2


xrange = np.arange(-np.pi, np.pi, np.pi/300)
yrange = np.arange(-np.pi, np.pi, np.pi/300)
X, Y = np.meshgrid(xrange,yrange)
M =  (X)**2 + (Y)**2 < 0.01 


plt.figure(1)
plt.subplot(321,aspect='equal') 
plt.title('Original')
plt.imshow(M)

D1 = fftpack.fft2(M)
D2 = fftpack.fftshift(D1)
abs_image = np.abs(D2)


plt.subplot(322,aspect='equal') 
plt.title('FFT')
plt.imshow(abs_image)

X, Y = np.meshgrid(xrange,yrange) 
M2 =  (X - 0.5)**2 + (Y - 0.5)**2 < 0.01 
M2 += (X + 0.5)**2 + (Y + 0.5)**2 < 0.01
M2 += (X - 0.5)**2 + (Y + 0.5)**2 < 0.01
M2 += (X + 0.5)**2 + (Y - 0.5)**2 < 0.01

plt.subplot(323,aspect='equal') 
plt.title('Original 4 Points')	
plt.imshow(M2)

D1 = fftpack.fft2(M2)
D2 = fftpack.fftshift(D1)
abs_image = np.abs(D2)


plt.subplot(324,aspect='equal') 
plt.title('FFT 4 Points')
plt.imshow(abs_image)

X, Y = np.meshgrid(xrange,yrange)
M3 = X + Y > 10000000 
pos = [-2.5,-2,-1.5,-1.0,-0.5,0,0.5,1.0,1.5,2.0,2.5]
for x in pos:
	for y in pos:
		M3 +=  (X + x)**2 + (Y + y)**2 < 0.01

plt.subplot(325,aspect='equal') 
plt.title('Original n Points')	
plt.imshow(M3)

D1 = fftpack.fft2(M3)
D2 = fftpack.fftshift(D1)
abs_image = np.abs(D2)


plt.subplot(326,aspect='equal') 
plt.title('FFT n Points')
plt.imshow(np.log(abs_image))

plt.show()