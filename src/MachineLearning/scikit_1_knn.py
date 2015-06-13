'''
Created on Jun 13, 2015

@author: rhf
'''

from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression


# import some data to play with
iris = datasets.load_iris()

##
print iris.target
print iris.target_names

X = iris.data
y = iris.target

##
print X.shape
print y.shape

# insantiate the estimator
knn1 = KNeighborsClassifier(n_neighbors=1)

knn1.fit(X, y)
p = knn1.predict([3,5,4,2])
print iris.target_names[p]
# ['virginica']

X_new = [[3,5,4,2],[5,4,3,2]]
p = knn1.predict(X_new)
print iris.target_names[p]
# ['virginica' 'versicolor']

knn5 = KNeighborsClassifier(n_neighbors=5)
knn5.fit(X, y)
p = knn5.predict(X_new)
print iris.target_names[p]
# ['versicolor' 'versicolor']


#
# Different Classification model
# 

logreg = LogisticRegression()
logreg.fit(X, y)
p = logreg.predict(X_new)
print iris.target_names[p]
# ['virginica' 'setosa']

