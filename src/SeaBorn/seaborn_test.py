from __future__ import division

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

titanic = pd.read_csv('data/titanic.csv')
print titanic.head()

#    PassengerId  Survived  Pclass  \
# 0            1         0       3
# 1            2         1       1
# 2            3         1       3
# 3            4         1       1
# 4            5         0       3
#
#                                                 Name     Sex  Age  SibSp  \
# 0                            Braund, Mr. Owen Harris    male   22      1
# 1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female   38      1
# 2                             Heikkinen, Miss. Laina  female   26      0
# 3       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female   35      1
# 4                           Allen, Mr. William Henry    male   35      0
#
#    Parch            Ticket     Fare Cabin Embarked
# 0      0         A/5 21171   7.2500   NaN        S
# 1      0          PC 17599  71.2833   C85        C
# 2      0  STON/O2. 3101282   7.9250   NaN        S
# 3      0            113803  53.1000  C123        S
# 4      0            373450   8.0500   NaN        S

# Age of the passagers in Titanic
plt.figure()
plt.hist(titanic.Age.dropna(), bins=25)

# Box plot
#plt.figure()
#sns.boxplot(titanic.Age.dropna(), titanic.Sex.dropna(), vert=False)

# Kernel density estimate
plt.figure()
sns.kdeplot(titanic.Age.dropna(), shade=True)

# Violin Plot
plt.figure()
sns.violinplot(titanic.Age.dropna(), titanic.Sex)

# cumulative distribution funtion
plt.figure()
sns.kdeplot(titanic.Age.dropna(), cumulative=True)


plt.show()
