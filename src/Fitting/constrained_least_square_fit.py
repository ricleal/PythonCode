import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


"""
Sequential Least SQuares Programming

"""

np.random.seed(42)

def peval(p, X):
    return np.dot(X, p)


def objective(p, y, X):
    return np.sum((y - peval(p, X)) ** 2)


def constraint(t):
    # sum must be zero, i.e., np.sum(t) == 0
    return np.sum(t)

# y = -2*x**2 + 2.5*x - 0.5
t = np.reshape(np.arange(100) * 0.1, (100, 1))
print "t shape:", t.shape
X = np.hstack([t ** 2, t ** 1, t ** 0])
print "X shape:", X.shape

ptrue = np.array([-2.0, 2.5, -0.5])
ytrue = peval(ptrue, X)
# add measurement noise
ymeas = ytrue + 10 * np.random.randn(len(ytrue))

# guess
p0 = np.zeros(3)
cons = {
    'type': 'eq',
    'fun': constraint,
}

res = optimize.minimize(objective,
                        p0,
                        args=(ymeas, X),
                        method='SLSQP',
                        constraints=cons,
                        options={'disp': True}  # print convergence messages.
                        )

pcons = res.x
yfit = peval(pcons, X)

ss_res = np.sum((ymeas - yfit) ** 2)
ss_tot = np.var(ymeas) * len(ymeas)
rsq = 1 - ss_res / ss_tot

print 'ss_res', ss_res
print 'ss_tot', ss_tot
print 'rsq', rsq

plt.plot(t, ymeas, 'o', t, ytrue, t, yfit)
plt.title('Least Squares Fit')
plt.legend(['Noisy Data', 'True', 'Fit'])
plt.show()
