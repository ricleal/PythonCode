import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq as optimizer

def rmsd(a,b):
    return np.sqrt((a-b)**2)

def func(x,A,k,theta):
    return A*np.sin(2*np.pi*k*x+theta)

x = np.arange(0, np.pi, np.pi/200)

A = 20
k = np.pi/12
theta = np.pi/6

y_true = func(x,A,k,theta)
y_meas = y_true + 2*np.random.randn(len(x))

def residuals(p, y, x):
    A,k,theta = p
    err = y-func(x,A,k,theta)
    return err

def peval(x, p):
    A,k,theta = p
    return func(x,A,k,theta)

p0 = [np.max(y_meas), np.pi/11, np.pi/3]
print 'Guess:\t',np.array(p0)
# [  8.      43.4783   1.0472]


plsq = optimizer(residuals, p0, args=(y_meas, x))
print 'Found:\t',plsq[0]
# [ 10.9437  33.3605   0.5834]

print 'Theor:\t',np.array([A, k, theta])
# [ 10.      33.3333   0.5236]

print 'RMSD :\t',rmsd(plsq[0], np.array([A, k, theta]))

plt.plot(x,peval(x,plsq[0]), label='Fit' )
plt.plot(x,y_meas,'x', label='Measured')
plt.plot(x,y_true , label='Theoretical')

plt.title('Least-squares fit to noisy data')
plt.legend()
plt.show()
