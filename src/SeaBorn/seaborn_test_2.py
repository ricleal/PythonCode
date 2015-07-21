import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#
# Auto
#

auto = pd.read_csv('data/auto.csv')
print auto.describe()

# Fig 1
#plt.figure()
sns.pairplot(auto, x_vars=['year','weight'],y_vars='mpg', size=7,aspect=0.7,kind='reg')

# Fig 2
plt.figure()
sns.kdeplot(auto.year, auto.mpg, shade=True);

# Fig 3
with sns.axes_style("white"):
    sns.jointplot("weight", "mpg", auto, kind="kde");

# Fig 4
plt.figure()
sns.distplot(auto.weight)
plt.show()
