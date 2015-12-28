import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, fftpack
from numpy import dtype

def pattern1():
    a = np.zeros([200,200])
    for (x,y),value in np.ndenumerate(a):
        if x>0 and y>0:
            if x%10 == 0 and y%10 == 0:
                a[x,y] = 10
            else:
                a[x,y] = 0.01
    return a

def pattern2():
    a = np.zeros([201,201])
    for (x,y),value in np.ndenumerate(a):
        if x%10 == 0 and y%10 == 0:
            a[x,y] = 10
        else:
            a[x,y] = 0.01
    return a

def pattern3():
    a = np.zeros([200,200])
    def radius(x,y):
        return np.sqrt(x**2+y**2)
    for (x,y),value in np.ndenumerate(a):
        if radius(x,y)%np.sqrt(4) == 0 :
            a[x,y] = 10
        else:
            a[x,y] = 0.01
    return a

def pattern4():
    a = np.zeros([200,200])
    def radius(x,y):
        return np.sqrt((x - a.shape[0]/2)**2 + (y - a.shape[1]/2)**2)
    for (x,y),value in np.ndenumerate(a):
        if radius(x,y)%np.sqrt(2) == 0 :
            a[x,y] = 10
        else:
            a[x,y] = 0.01
    return a


def pattern5():
    a = np.zeros([200,200])
    for (x,y),value in np.ndenumerate(a):
        if x%10 == 0 or y%10 == 0 :
            a[x,y] = 10
        else:
            a[x,y] = 0.01
    return a

a = pattern4()


plt.figure(1)
plt.subplot(221)
plt.title('Original')
plt.imshow(np.log(a), cmap='gray')

F = np.fft.fft2(a)

im_shift = np.log(np.abs(np.fft.fftshift(F))**2)
plt.subplot(222)
plt.title('fftshift')
plt.imshow(im_shift, cmap='gray')

im_real = np.log(F.real)
plt.subplot(223)
plt.title('real')
plt.imshow(im_real, cmap='gray')

im_imag = np.log(F.imag)
plt.subplot(224)
plt.title('imag')
plt.imshow(im_imag, cmap='gray')


plt.show()
