import numpy as np
import matplotlib.pyplot as plt


# Example 1
x = np.linspace(-1, 1, 2000)
y = np.cos(x) + 0.3*np.random.rand(2000)

p = np.polynomial.Chebyshev.fit(x, y, deg=50)
t = np.linspace(-1, 1, 200)

plt.plot(x, y, 'r.')
plt.plot(t, p(t), 'k-', lw=3)   



# Example 2



# End

plt.show()