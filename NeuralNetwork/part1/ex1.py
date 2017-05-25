import numpy as np
from pprint import pprint, pformat

# input
X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ])
print('Input X:\n', pformat(X))

# output
y = np.array([[0,1,1,0]]).T
print('Output y:\n', pformat(y))

syn0 = 2*np.random.random((3,4)) - 1
print('syn0:\n', pformat(syn0))

syn1 = 2*np.random.random((4,1)) - 1
print('syn1:\n', pformat(syn1))

for j in range(60000):
    l1 = 1/(1+np.exp(-(np.dot(X,syn0))))
    l2 = 1/(1+np.exp(-(np.dot(l1,syn1))))
    l2_delta = (y - l2)*(l2*(1-l2))
    l1_delta = l2_delta.dot(syn1.T) * (l1 * (1-l1))
    syn1 += l1.T.dot(l2_delta)
    syn0 += X.T.dot(l1_delta)

print('Done L1:\n', pformat(l1))