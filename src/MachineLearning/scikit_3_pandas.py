'''
Created on Jun 13, 2015

@author: rhf
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import numpy as np

data = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv',index_col=0)
print data.head()

# Features: TV, Radio, Newspaper
# Response: Sales

# Plot:
sns.pairplot(data, x_vars=['TV','Radio','Newspaper'],y_vars='Sales', size=7,aspect=0.7,kind='reg')
#plt.show()

##
## Linear regression

feature_cols = ['TV','Radio','Newspaper']
X = data[feature_cols]
y = data['Sales']

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1) # no random split each time!

linreg = LinearRegression()
linreg.fit(X_train, y_train)

print linreg.intercept_
print linreg.coef_
print zip(feature_cols,linreg.coef_)

y_pred = linreg.predict(X_test)
print 'ERROR:', metrics.median_absolute_error(y_test,y_pred)
print 'RMSE:', np.sqrt(metrics.mean_squared_error(y_test,y_pred))

#
#
#

plt.show()

