'''
Created on Jun 13, 2015

@author: rhf
'''

from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.cross_validation import train_test_split

# import some data to play with
iris = datasets.load_iris()

X = iris.data
y = iris.target # response vector

logreg = LogisticRegression()
logreg.fit(X, y)
y_pred = logreg.predict(X)
print 'logreg:', metrics.accuracy_score(y, y_pred)
# 0.96 # 96% are correced predicted!

knn1 = KNeighborsClassifier(n_neighbors=1)
knn1.fit(X, y)
y_pred = knn1.predict(X)
print 'knn1:', metrics.accuracy_score(y, y_pred)
# 1.0

knn5 = KNeighborsClassifier(n_neighbors=5)
knn5.fit(X, y)
y_pred = knn5.predict(X)
print 'knn5:', metrics.accuracy_score(y, y_pred)
# 0.966666666667


#
# train / test split
#

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.4, 
                                                    random_state=4) # no random split each time!

logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)
print 'logreg:', metrics.accuracy_score(y_test, y_pred)

knn1.fit(X_train, y_train)
y_pred = knn1.predict(X_test)
print 'knn1:', metrics.accuracy_score(y_test, y_pred)

knn5.fit(X_train, y_train)
y_pred = knn5.predict(X_test)
print 'knn5:', metrics.accuracy_score(y_test, y_pred)

