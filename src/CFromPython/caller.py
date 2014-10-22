import c_module as c

print dir(c)


import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as k

x = np.linspace(-k.pi,k.pi,100)
y1 = np.zeros(x.shape)
y2 = np.zeros(x.shape)

for idx,i in enumerate(x):
    y1[idx]= c.cos_func(i)
    y2[idx]= c.sin_func(i)

plt.plot(x, y1, '.')
plt.plot(x, y2, 'x')
plt.show()