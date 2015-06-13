import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
import statsmodels.formula.api as smf
import numpy as np

boston = load_boston()

print boston.DESCR

column_names = [
        'CRIM',     #per capita crime rate by town
        'ZN',       #proportion of residential land zoned for lots over 25,000 sq.ft.
        'INDUS',    #proportion of non-retail business acres per town
        'CHAS',     #Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
        'NOX',      #nitric oxides concentration (parts per 10 million)
        'RM',       #average number of rooms per dwelling
        'AGE',      #proportion of owner-occupied units built prior to 1940
        'DIS',      #weighted distances to five Boston employment centres
        'RAD',      #index of accessibility to radial highways
        'TAX',      #full-value property-tax rate per $10,000
        'PTRATIO',  #pupil-teacher ratio by town
        'B',       # 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
        'LSTAT']  #  % lower status of the population
       # 'MEDV'] #     Median value of owner-occupied homes in $1000's

df = pd.DataFrame(boston.data, columns=column_names)
df['MEDV'] = boston.target

plt.scatter(df.CRIM, df.MEDV)
plt.xlabel("crime")
plt.ylabel("home value")

results = smf.ols(formula='standardize(MEDV) ~ C(CRIM)', data=df).fit()
print results.summary()

xs = np.linspace(0, df.CRIM.max(), 100)
plt.plot(xs, xs*results.params[0], 'r--')



plt.show()