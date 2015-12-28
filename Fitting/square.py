import numpy as np

# create Array
nx, ny = (10, 10)
x = np.linspace(1, 10, nx)
y = np.linspace(1, 10, ny)
xv, yv = np.meshgrid(x, y)

ra = np.random.rand(nx, ny) - 0.5

# Solve a x = b

a = yv + ra
b = yv

x = np.linalg.solve(a, b)


# Check solution
np.allclose(np.dot(a, x), b)


import numpy as np
import matplotlib.pyplot as plt



plt.figure(1)
plt.subplot(311)
plt.plot(xv, a, 'o')
plt.xlim([0,11])
plt.ylim([0,11])
plt.title("A")

plt.subplot(312)
plt.plot(xv, b, 'o')
plt.xlim([0,11])
plt.ylim([0,11])
plt.title("B")

plt.subplot(313)
plt.plot(xv, x, 'o')
plt.xlim([0,11])
#plt.ylim([0,11])
plt.title("X")

plt.show()