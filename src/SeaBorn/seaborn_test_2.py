import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#
# Auto
#

auto = pd.read_csv('data/auto.csv')
print auto.describe()

#plt.figure()
sns.pairplot(auto, x_vars=['year','weight'],y_vars='mpg', size=7,aspect=0.7,kind='reg')

plt.figure()
sns.kdeplot(auto.year, auto.mpg, shade=True);

with sns.axes_style("white"):
    sns.jointplot("weight", "mpg", auto, kind="kde");

plt.figure()
sns.distplot(auto.weight)  
plt.show()