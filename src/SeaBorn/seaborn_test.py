import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

titanic = pd.read_csv('data/titanic.csv')

# Age of the passagers in Titanic
plt.figure()
plt.hist(titanic.Age.dropna(), bins=25)

# Box plot
plt.figure()
sns.boxplot(titanic.Age, titanic.Sex, vert=False)

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