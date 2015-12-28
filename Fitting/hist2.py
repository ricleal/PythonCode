import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

list = np.random.randn(1000)

plt.figure(1)
result = plt.hist(list, 50)
plt.xlim((min(list), max(list)))

mean = np.mean(list)
variance = np.var(list)
sigma = np.sqrt(variance)
x = np.linspace(min(list), max(list),100)
dx = result[1][1] - result[1][0]
scale = len(list)*dx
plt.plot(x, mlab.normpdf(x,mean,sigma)*scale)

plt.show()
