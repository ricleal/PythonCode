import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, fftpack

def dist(a,b):
    return np.linalg.norm(a-b)

def find_vectors_slow(a):
    vects = []
    for (x,y),value in np.ndenumerate(a):
        if value > 0:
            for (x2,y2),value2 in np.ndenumerate(a):
                if value2 > 0:
                    d = dist(np.array([x,y]),
                             np.array([x2,y2]) )
                    if d not in vects:
                        vects.append(d)
    return vects

# NOT WORKING!!
def find_vectors(a):
    vects = []
    for (x,y),value in np.ndenumerate(a):
        if value > 0:
           vects.append((x,y)) 
    spot_coords = np.matrix(vects)
    dot_prod = np.dot(spot_coords, spot_coords.T)
    dot_prod_combinations = dot_prod[np.triu_indices_from(spot_coords, k=1)]
    norm = np.sqrt(dot_prod_combinations)
    return norm

def pattern1(a):
    for (x,y),value in np.ndenumerate(a):
        if x>0 and y>0:
            if x%10 == 0 and y%10 == 0:
                a[x,y] = 100
            else:
                a[x,y] = 0.01
    return a

def pattern2(a):
    for (x,y),value in np.ndenumerate(a):
        if x%10 == 0 and y%10 == 0:
            a[x,y] = 100
        else:
            a[x,y] = 0.01
    return a

a = np.zeros([100,100])

a = pattern1(a)

    

# vectors = find_vectors(a)
# vectors.sort()
# print vectors

plt.figure(1)
plt.subplot(121)
plt.imshow(np.log(a), cmap='gray')
plt.colorbar()


F = np.fft.fft2(a)
im = np.log(np.abs(np.fft.fftshift(F))**2)


plt.subplot(122)
plt.imshow(im, cmap='gray')
plt.colorbar()
plt.show()
